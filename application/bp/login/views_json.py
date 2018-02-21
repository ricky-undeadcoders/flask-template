#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import (g, jsonify, render_template, flash, current_app, get_flashed_messages)
from flask_security import current_user, login_required

from application.bp.login.forms import (ChangePasswordForm,
                                        UserSettingsChangeNameForm,
                                        ModifyAndConfirmEmailForm,
                                        UserSettingsChangeUserNameForm,
                                        ForgotPasswordForm)
from application.bp.login.utils import send_reset_password_instructions


@login_required
def user_settings_change_password():
    try:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success')}), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to update password; error: {}'.format(e))
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@login_required
def user_settings_change_name():
    try:
        form = UserSettingsChangeNameForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success')}), 200, {}
    except Exception, e:
        current_app.logger.critical('Fatal error changing first and last name; error: {}'.format(e))
        return jsonify({'message_modal': get_flashed_messages(category_filter='error')}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@login_required
def user_settings_change_username():
    try:
        form = UserSettingsChangeUserNameForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success')}), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to update password; error: {}'.format(e))
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@login_required
def modify_and_confirm_email():
    # TODO: We need to send an email confirmation for this to allow the email update
    try:
        form = ModifyAndConfirmEmailForm()
        if form.validate_on_submit():
            if form.update_cache_data():
                return jsonify({'message': get_flashed_messages(category_filter='success')}), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to update password; error: {}'.format(e))
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


def forgot_password_exec():
    try:
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            send_reset_password_instructions(form.user)
            return jsonify({'message': get_flashed_messages(category_filter='success')}), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to submit forgot password; error: {}'.format(e))
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}
