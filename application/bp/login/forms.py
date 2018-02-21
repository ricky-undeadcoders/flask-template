#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import (request, current_app, g, url_for, flash)
from flask_wtf import RecaptchaField
from flask_security import current_user, login_user, logout_user
from flask_security.confirmable import requires_confirmation, confirm_email_token_status
from flask_security.utils import verify_and_update_password, do_flash, get_message, config_value
from wtforms import (StringField, PasswordField, BooleanField, SubmitField)
from wtforms.validators import (DataRequired, EqualTo, Email, Length, Regexp)

from application.config import (datastore_config as ds_config,
                                verbiage_config as v_config)
from application.config.password import password_config
from application.bp.login.utils import (Password, register_user, send_confirmation_instructions, change_user_password)
from application.bp.login.redis_utils import get_new_email, set_new_email
from application.forms import CustomForm


class ChangePasswordForm(CustomForm):
    new_password = PasswordField(label='New Password',
                                 validators=[DataRequired(),
                                             EqualTo('confirm_password',
                                                     message=password_config.PASSWORD_NOT_MATCH_ERROR),
                                             Regexp(regex=ds_config.USER_PASSWORD_REGEX,
                                                    message=password_config.PASSWORD_INVALID_CHARACTER_ERROR)])
    confirm_password = PasswordField(label='Confirm New Password',
                                     validators=[DataRequired(),
                                                 EqualTo('new_password',
                                                         message=password_config.PASSWORD_NOT_MATCH_ERROR),
                                                 Regexp(regex=ds_config.USER_PASSWORD_REGEX,
                                                        message=password_config.PASSWORD_INVALID_CHARACTER_ERROR)])
    current_password = PasswordField(label='Current Password',
                                     validators=[DataRequired()])

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = current_app.config['PASSWORD_UPDATED_SUCCESS_MESSAGE']

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.user = current_user
        password = Password(password=self.new_password.data,
                            old_password=self.current_password.data,
                            user=current_user)
        if not password.verify_and_update():
            self.new_password.errors.append(password.error_list)
            return self.validation_error()
        if self.new_password.data.strip() == self.current_password.data.strip():
            self.current_password.errors.append(current_app.config['MSG_TEXT_NOT_CHANGED'])
            return self.validation_error()
        self.validated = True
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            return self.validation_error()
        current_app.logger.info('Attempting to change users password: {}'.format(current_user.id))
        change_user_password(user=current_user, password=self.new_password.data)
        current_app.logger.info('Successfully updated users password')
        return self.update_success()


class UserSettingsChangeNameForm(CustomForm):
    first_name = StringField(label='First Name', validators=[Length(max=ds_config.USER_FIRST_NAME_MAX_LENGTH),
                                                             Regexp(regex=ds_config.USER_FIRST_NAME_REGEX,
                                                                    message=v_config.ALPHABET_ONLY)])
    last_name = StringField(label='Last Name', validators=[Length(max=ds_config.USER_LAST_NAME_MAX_LENGTH),
                                                           Regexp(regex=ds_config.USER_LAST_NAME_REGEX,
                                                                  message=v_config.ALPHABET_ONLY)])

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = current_app.config['NAME_UPDATED_SUCCESS_MESSAGE']

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.user = current_user
        if self.first_name.data != self.user.first_name:
            self.kwargs.update({'first_name': self.first_name.data})
        if self.last_name.data != self.user.last_name:
            self.kwargs.update({'last_name': self.last_name.data})
        if len(self.kwargs) == 0:
            self.first_name.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()

        current_app.logger.info(
            'Attempting to update user\'s name from {} {} to {} {}'.format(self.user.first_name,
                                                                           self.user.last_name,
                                                                           self.first_name.data,
                                                                           self.last_name.data))

        user = g.datastore.modify_user(user=self.user, **self.kwargs)
        if user:
            current_app.logger.info('Successfully updated name')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating user')
            return self.update_error()


class UserSettingsChangeUserNameForm(CustomForm):
    username = StringField(label='Username', validators=[Length(max=ds_config.USER_USERNAME_MAX_LENGTH),
                                                         Regexp(regex=ds_config.USER_USERNAME_REGEX,
                                                                message=v_config.ALPHANUMERIC_UNDERSCORE_PERIOD_ONLY)])

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = current_app.config['USERNAME_UPDATED_SUCCESS_MESSAGE']

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.user = current_user
        if self.username.data != self.user.username:
            self.kwargs.update({'username': self.username.data})
        if len(self.kwargs) == 0:
            self.username.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()

        current_app.logger.info(
            'Attempting to update username from {} to {}'.format(self.user.username,
                                                                 self.username.data))

        user = g.datastore.modify_user(user=self.user, **self.kwargs)
        if user:
            current_app.logger.info('Successfully updated username')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating username')
            return self.update_error()


class ModifyAndConfirmEmailForm(CustomForm):
    email = StringField(label='Email', validators=[Length(max=ds_config.USER_EMAIL_MAX_LENGTH),
                                                   Email()])

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.new_email = None
        self.success_message = current_app.config['EMAIL_CHANGE_CONFIRMATION_SENT']

    def validate_on_submit(self):
        '''
        add requested email to the cache, delete based off config point
        :return:
        '''
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        if g.datastore.find_user(email=self.email.data):
            flash(current_app.config['EMAIL_ALREADY_EXISTS'], 'error')
            return self.validation_error()
        self.user = current_user
        if self.email.data != self.user.email:
            self.kwargs.update({'email': self.email.data})
        if len(self.kwargs) == 0:
            self.email.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()
        return self.validation_success()

    def update_cache_data(self):
        send_confirmation_instructions(self.user, email=self.email.data)
        set_new_email(user=self.user, email=self.email.data)

        current_app.logger.info('Successfully sent confirmation email')
        return self.update_success()

    def validate_cache_data(self, token):
        self.success_message = current_app.config['SECURITY_MSG_EMAIL_CONFIRMED'][0]
        expired, invalid, self.user = confirm_email_token_status(token)
        self.new_email = get_new_email(self.user)
        if not self.new_email:
            flash('Unable to retrieve old email, please try updating your email address again', 'error')
            return self.update_error()
        if not self.user or invalid:
            do_flash(*get_message('INVALID_CONFIRMATION_TOKEN'))
            return self.update_error()
        if expired:
            send_confirmation_instructions(self.user, )
            do_flash(*get_message('CONFIRMATION_EXPIRED', email=self.user.email,
                                  within=config_value('CONFIRM_EMAIL_WITHIN')))
            return self.update_error()

        if self.user != current_user:
            logout_user()
            login_user(self.user)

        return self.validation_success()

    def update_data(self):
        current_app.logger.info(
            'Attempting to update email from {} to {}'.format(self.user.email,
                                                              self.new_email))

        user = g.datastore.modify_user(user=self.user, email=self.new_email)
        if user:
            current_app.logger.info('Successfully updated email')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating email')
            return self.update_error()


class LoginForm(CustomForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.remember.default = current_app.config['SECURITY_DEFAULT_REMEMBER_ME']
        self.user = None

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()

        self.user = g.datastore.find_user(username=self.username.data)

        if self.user is None:
            self.user = g.datastore.find_user(email=self.username.data)

        if self.user is None:
            self.username.errors.append(current_app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'][0])
            return self.validation_error()
        if not self.user.password:
            self.password.errors.append(current_app.config['SECURITY_MSG_PASSWORD_NOT_SET'][0])
            return self.validation_error()
        if not verify_and_update_password(self.password.data, self.user):
            self.password.errors.append(current_app.config['SECURITY_MSG_INVALID_PASSWORD'][0])
            return self.validation_error()
        if requires_confirmation(self.user):
            do_flash(*get_message('CONFIRMATION_REQUIRED'))
            return self.validation_error()
        if not self.user.is_active:
            do_flash(*current_app.config['SECURITY_MSG_DISABLED_ACCOUNT'])
            return self.validation_error()
        return self.validation_success()


class RegisterUserForm(CustomForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    username = StringField(validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField()
    last_name = StringField()
    captcha = RecaptchaField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.success_message = 'You have been successfully registered! Please check your email to log in.'
        self.user = None

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()

        if current_app.config['REGISTRATION_BY_INVITE_ONLY']:
            if not g.datastore.find_invitation_email(email=self.email.data):
                do_flash(*current_app.config['MSG_REGISTRATION_BY_INVITE_ONLY'])
                return self.validation_error()

        user = g.datastore.find_user(email=self.email.data)
        if user:
            self.email.errors.append(current_app.config['MSG_EMAIL_CLAIMED'])
            return self.validation_error()
        user = g.datastore.find_user(username=self.username.data)
        if user:
            self.email.errors.append(current_app.config['MSG_USERNAME_CLAIMED'])
            return self.validation_error()
        if self.email.data:
            self.kwargs['email'] = self.email.data
        if self.password.data:
            self.kwargs['password'] = self.password.data
        if self.first_name.data:
            self.kwargs['first_name'] = self.first_name.data
        if self.last_name.data:
            self.kwargs['last_name'] = self.last_name.data
        if self.username.data:
            self.kwargs['username'] = self.username.data

        return self.validation_success()

    def update_data(self):
        self.user = register_user(**self.kwargs)
        return self.update_success()


class ResendConfirmationForm(CustomForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    captcha = RecaptchaField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.success_message = 'Confirmation Sent!'
        self.user = None

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()

        self.user = g.datastore.find_user(email=self.email.data)
        if not self.user:
            do_flash(*current_app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'])
            return self.validation_error()

        return self.validation_success()

    def update_data(self):
        self.user = send_confirmation_instructions(self.user)
        return self.update_success()


class ForgotPasswordForm(CustomForm):
    """The default forgot password form"""

    email = StringField(label='Email', validators=[DataRequired(), Email()])
    captcha = RecaptchaField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.success_message = 'Instructions to reset your password have been sent to your email!'
        self.user = None

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()

        self.user = g.datastore.find_user(email=self.email.data)
        if not self.user:
            self.email.errors.append('Email Not Found')
            return self.validation_error()
        if requires_confirmation(self.user):
            do_flash(*get_message('CONFIRMATION_REQUIRED'))
            return self.validation_error()
        return self.update_success()


class ResetPasswordForm(CustomForm):
    new_password = PasswordField(label='New Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField(label='Confirm New Password',
                                     validators=[DataRequired(), EqualTo('new_password')])

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        return self.validation_success()
