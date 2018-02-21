#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import url_for, current_app, g, flash
from flask_security.utils import verify_and_update_password, hash_password, get_message
from flask_security.recoverable import (generate_reset_password_token, config_value)
from flask_security.signals import (reset_password_instructions_sent, password_reset, user_registered,
                                    confirm_instructions_sent, password_changed)
from flask_security.confirmable import generate_confirmation_token

from application.config.password import (restricted_partial_word_list,
                                         restricted_word_list,
                                         password_config as p_config)
from application.utils import send_mail


class Password(object):
    def __init__(self, password, old_password=None, user=None):
        self.old_password = old_password
        self.password = password
        self.user = user
        self.clean_password = self.password.lower().strip()
        self.error_list = []

    def verify_and_update(self):
        if self.is_valid:
            if not verify_and_update_password(password=self.old_password,
                                              user=self.user):
                self.error_list.append(p_config.INCORRECT_PASSWORD_ERROR)
                return False
            return True

    @property
    def is_valid(self):
        if all([self.is_correct_length()]):
            return True
        return False

    def is_clean(self):
        for word in restricted_partial_word_list:
            if word in self.clean_password:
                self.error_list.append(p_config.PASSWORD_WORD_INCLUSION_ERROR)
                return False
        for word in restricted_word_list:
            if word == self.clean_password:
                self.error_list.append(p_config.PASSWORD_WORD_MATCH_ERROR)
                return False

        return True

    def is_correct_length(self):
        password_length = len(self.clean_password)
        if any([password_length < p_config.PASSWORD_MIN_LENGTH, password_length > p_config.PASSWORD_MAX_LENGTH]):
            self.error_list.append(p_config.PASSWORD_LENGTH_ERROR)
            return False

        return True


def send_reset_password_instructions(user):
    """Sends the reset password instructions email for the specified user.

    :param user: The user to send the instructions to
    """
    token = generate_reset_password_token(user)
    reset_link = url_for(
        'login.reset_password', token=token, _external=True
    )

    if config_value('SEND_PASSWORD_RESET_EMAIL'):
        send_mail(config_value('EMAIL_SUBJECT_PASSWORD_RESET'), [user.email],
                  'reset_instructions',
                  user=user, reset_link=reset_link)

    reset_password_instructions_sent.send(
        current_app._get_current_object(), user=user, token=token
    )


def send_password_reset_notice(user):
    """Sends the password reset notice email for the specified user.

    :param user: The user to send the notice to
    """
    if config_value('SEND_PASSWORD_RESET_NOTICE_EMAIL'):
        send_mail(config_value('EMAIL_SUBJECT_PASSWORD_NOTICE'), [user.email],
                  'reset_notice', user=user)


def update_password(user, password):
    """Update the specified user's password

    :param user: The user to update_password
    :param password: The unhashed new password
    """
    user.password = hash_password(password)
    g.datastore.modify_user(user)
    send_password_reset_notice(user)
    password_reset.send(current_app._get_current_object(), user=user)


def register_user(**kwargs):
    security = current_app.extensions.get('security')
    confirmation_link, token = None, None
    kwargs['password'] = hash_password(kwargs['password'])
    user = g.datastore.create_user(**kwargs)

    if security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        flash(*get_message('CONFIRM_REGISTRATION', email=user.email))

    user_registered.send(current_app._get_current_object(),
                         user=user, confirm_token=token)

    if config_value('SEND_REGISTER_EMAIL'):
        send_mail(config_value('EMAIL_SUBJECT_REGISTER'), [user.email],
                  'welcome', user=user, confirmation_link=confirmation_link)

    return user


def generate_confirmation_link(user, confirmation_url=None):
    if not confirmation_url:
        confirmation_url = 'login.confirm_email'
    token = generate_confirmation_token(user)
    return url_for(confirmation_url, token=token, _external=True), token


def send_confirmation_instructions(user, email=None):
    """Sends the confirmation instructions email for the specified user.
    :param user: The user to send the instructions to
    :param email: if sending to an email address other than the user's primary
        - email is currently only used when changing a user's email, so we send to the new address
    """
    confirmation_url = None
    if not email:
        email = user.email
    else:
        confirmation_url = 'login.confirm_email_modification'

    confirmation_link, token = generate_confirmation_link(user, confirmation_url=confirmation_url)

    send_mail(config_value('EMAIL_SUBJECT_CONFIRM'), [email],
              'confirmation_instructions', user=user,
              confirmation_link=confirmation_link)

    confirm_instructions_sent.send(current_app._get_current_object(), user=user,
                                   token=token)


def change_user_password(user, password):
    """Change the specified user's password

    :param user: The user to change_password
    :param password: The unhashed new password
    """
    user.password = hash_password(password)
    g.datastore.modify_user(user)
    send_password_changed_notice(user)
    password_changed.send(current_app._get_current_object(),
                          user=user)


def send_password_changed_notice(user):
    send_mail(config_value(['EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE']), [user.email],
              'change_notice')
