#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import (redirect, url_for, current_app, flash, g, jsonify, get_flashed_messages)
from flask_security import login_required, roles_required

from application.login_decorators import admin_login_required
from application.bp.admin.forms import (ModifyAdminUserForm,
                                        ModifyUserForm,
                                        AddAdminUserForm,
                                        AddUserForm,
                                        ModifyRoleForm,
                                        AddRoleForm,
                                        ModifyAdminRoleForm,
                                        AddAdminRoleForm,
                                        ContentDraftImageForm,
                                        ContentDraftTextForm,
                                        ContentPublishForm,
                                        AddFAQForm,
                                        ModifyFAQForm)
from application.bp.login.forms import ChangePasswordForm


@admin_login_required
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


@admin_login_required
def modify_user():
    try:
        form = ModifyUserForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to modify user; error: {}'.format(e))
        return jsonify({'message_modal': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@admin_login_required
def modify_admin_user():
    try:
        form = ModifyAdminUserForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to modify user; error: {}'.format(e))
        return jsonify({'message': [{'error': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}]}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@admin_login_required
def add_user():
    try:
        form = AddUserForm()
        if form.validate_on_submit():
            if form.update_data():
                current_app.logger.info('Successfully added user')
    except Exception, e:
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')
        current_app.logger.error('Fatal error attempting to add user; error: {}'.format(e))

    return redirect(url_for('admin.users'))


@admin_login_required
def add_admin_user():
    try:
        form = AddAdminUserForm()
        if form.validate_on_submit():
            if form.update_data():
                current_app.logger.info('Successfully added admin user')
    except Exception, e:
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')
        current_app.logger.error('Fatal error attempting to add admin user; error: {}'.format(e))

    return redirect(url_for('admin.admin_users'))


@admin_login_required
def add_role():
    try:
        form = AddRoleForm()
        if form.validate_on_submit():
            if form.update_data():
                current_app.logger.info('Successfully added role')
    except Exception, e:
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')
        current_app.logger.error('Fatal error attempting to add role; error: {}'.format(e))

    return redirect(url_for('admin.roles'))


@admin_login_required
def modify_role():
    try:
        form = ModifyRoleForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to modify role; error: {}'.format(e))
        return jsonify({'message': [{'error': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}]}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@admin_login_required
def add_admin_role():
    try:
        form = AddAdminRoleForm()
        if form.validate_on_submit():
            if form.update_data():
                current_app.logger.info('Successfully added user')
    except Exception, e:
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')
        current_app.logger.error('Fatal error attempting to add role; error: {}'.format(e))

    return redirect(url_for('admin.admin_roles'))


@admin_login_required
def modify_admin_role():
    try:
        form = ModifyAdminRoleForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to modify user; error: {}'.format(e))
        return jsonify({'message': [{'error': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}]}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@admin_login_required
def add_faq():
    try:
        form = AddFAQForm()
        if form.validate_on_submit():
            if form.update_data():
                current_app.logger.info('Successfully added faq')
    except Exception, e:
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')
        current_app.logger.error('Fatal error attempting to add faq; error: {}'.format(e))

    return redirect(url_for('admin.faq'))


@admin_login_required
def modify_faq():
    try:
        form = ModifyFAQForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to modify faq; error: {}'.format(e))
        return jsonify({'message': [{'error': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}]}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@admin_login_required
def modify_content():
    try:
        form = ContentDraftTextForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to upload quill html; error: {}'.format(e))
        return jsonify({'message': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@admin_login_required
def upload_content_image():
    try:
        form = ContentDraftImageForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to upload quill html; error: {}'.format(e))
        return jsonify({'message': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}


@admin_login_required
def publish_content():
    try:
        form = ContentPublishForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to upload quill html; error: {}'.format(e))
        return jsonify({'message': current_app.config['GENERIC_FORM_ERROR_MESSAGE']}), 500, {}

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}
