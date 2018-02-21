#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask import (render_template, request, current_app, redirect, url_for, flash, g, session)
from flask_security import (login_required, login_user, logout_user, current_user)
from flask_security.decorators import anonymous_user_required
from flask_security.recoverable import (reset_password_token_status)
from flask_security.confirmable import (confirm_email_token_status, confirm_user)
from flask_security.utils import get_message, get_url, config_value, do_flash

from application.bp.login.forms import (ChangePasswordForm,
                                        UserSettingsChangeNameForm,
                                        ModifyAndConfirmEmailForm,
                                        UserSettingsChangeUserNameForm,
                                        RegisterUserForm,
                                        ForgotPasswordForm,
                                        ResetPasswordForm,
                                        ResendConfirmationForm)
from application.bp.login.utils import (update_password, send_confirmation_instructions)
from application.bp.login.redis_utils import get_new_email


@anonymous_user_required
def login():
    """View function for login view"""
    form = current_app.config['LOGIN_FORM']()
    if request.method.lower() == 'post':
        if form.validate_on_submit():
            current_app.logger.info('Form validated, logging in user')
            login_user(form.user, remember=form.remember.data)
            try:
                next = session.pop('next')
                resp = redirect(url_for(next))
            except Exception, e:
                current_app.logger.error('Unable to get next stop from request cookies: {}'.format(e))
                resp = redirect(url_for('main.index'))
            return resp

    return render_template('login/login.html',
                           login_user_form=form)


def logout():
    """View function which handles a logout request."""
    if current_user.is_authenticated:
        logout_user()
    return redirect(request.args.get('next', None) or url_for('main.index'))


@login_required
def user_settings():
    return render_template('login/user_settings/user_settings.html',
                           name_form=UserSettingsChangeNameForm(),
                           password_form=ChangePasswordForm(),
                           username_form=UserSettingsChangeUserNameForm(),
                           email_form=ModifyAndConfirmEmailForm())


@anonymous_user_required
def register():
    form = RegisterUserForm()
    if request.method.lower() == 'post':
        try:
            if form.validate_on_submit():
                if form.update_data():
                    current_app.logger.exception('Updated data successfully, in register')
                    security = current_app.extensions.get('security')
                    if not security.confirmable:
                        login_user(form.user)
                    return redirect(url_for('login.login'))

        except Exception, e:
            current_app.logger.error('Fatal error attempting to register user: {}'.format(e))
            flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return render_template('login/register_user.html',
                           register_user_form=form)


@anonymous_user_required
def confirm_email(token):
    """View function which handles a email confirmation request."""
    security = current_app.extensions.get('security')
    expired, invalid, user = confirm_email_token_status(token)

    if not user or invalid:
        invalid = True
        do_flash(*get_message('INVALID_CONFIRMATION_TOKEN'))
    if expired:
        send_confirmation_instructions(user)
        do_flash(*get_message('CONFIRMATION_EXPIRED', email=user.email,
                              within=security.confirm_email_within))
    if invalid or expired:
        return redirect(get_url(security.confirm_error_view) or
                        url_for('send_confirmation'))

    if user != current_user:
        logout_user()
        login_user(user)

    if confirm_user(user):
        msg = 'EMAIL_CONFIRMED'
    else:
        msg = 'ALREADY_CONFIRMED'

    do_flash(*get_message(msg))

    return redirect(get_url(security.post_confirm_view) or
                    get_url(security.post_login_view))


@login_required
def confirm_email_modification(token):
    """View function which handles a email confirmation request."""
    form = ModifyAndConfirmEmailForm()
    try:
        if form.validate_cache_data(token):
            if form.update_data():
                current_app.logger.info('Successfully updated email')
    except Exception, e:
        current_app.logger.error('Fatal error attempting to confirm_email_modification; error: {}'.format(e))
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return redirect(get_url('login.user_settings'))


def resend_confirmation_email():
    form = ResendConfirmationForm()
    try:
        if form.validate_on_submit():
            if form.update_data():
                return redirect(url_for('login.login'))
    except Exception, e:
        current_app.logger.error('Fatal error attempting to resend confirmation email; error: {}'.format(e))
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return render_template('login/resend_confirmation_email.html', confirm_form=form)


@anonymous_user_required
def forgot_password():
    form = ForgotPasswordForm()
    return render_template('login/forgot_password.html',
                           forgot_password_form=form)


@anonymous_user_required
def reset_password(token):
    """View function that handles a reset password request."""

    expired, invalid, user = reset_password_token_status(token)

    if invalid:
        do_flash(*get_message('INVALID_RESET_PASSWORD_TOKEN'))
    if expired:
        do_flash(*get_message('PASSWORD_RESET_EXPIRED', email=user.email,
                              within=config_value('RESET_PASSWORD_WITHIN')))
    if invalid or expired:
        return redirect(url_for('login.forgot_password'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        update_password(user, form.new_password.data)
        do_flash(*get_message('PASSWORD_RESET'))
        login_user(user)
        return redirect(get_url(config_value('POST_RESET_VIEW')) or
                        get_url(config_value('POST_LOGIN_VIEW')))

    else:
        current_app.logger.error('Form did not validate: {}'.format(form.errors))
        flash(form.errors, 'error')

    return render_template('login/reset_password.html',
                           reset_password_form=form,
                           reset_password_token=token)
