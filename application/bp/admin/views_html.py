#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from flask import (g, render_template, request, current_app, redirect, url_for, flash, send_from_directory, session)
from flask_security import (login_user, logout_user, current_user)
from flask_security.decorators import anonymous_user_required
from os import path

from application.login_decorators import admin_login_required
from application.bp.admin.decorators import generate_pagination
from application.bp.admin.forms import (ModifyUserForm,
                                        ModifyAdminUserForm,
                                        AddUserForm,
                                        AddAdminUserForm,
                                        AddRoleForm,
                                        ModifyRoleForm,
                                        ModifyAdminRoleForm,
                                        AddAdminRoleForm,
                                        ContentDraftTextForm,
                                        ContentDraftImageForm,
                                        ContentPublishForm,
                                        SearchForm,
                                        BulkDeleteForm,
                                        AddFAQForm,
                                        ModifyFAQForm)
from application.bp.login.forms import ChangePasswordForm


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
                resp = redirect(url_for('admin.dashboard'))
            return resp
        else:
            current_app.logger.error('Form did not validate: {}'.format(form.errors))
            flash(form.errors, 'error')

    return render_template('admin/login.html',
                           login_user_form=form)


@admin_login_required
def logout():
    """View function which handles a logout request."""
    if current_user.is_authenticated:
        logout_user()
    return redirect(request.args.get('next', None) or url_for('admin.login'))


@admin_login_required
def user_settings():
    return render_template('admin/user_settings/user_settings.html',
                           password_form=ChangePasswordForm())


@admin_login_required
def dashboard():
    return render_template('admin/dashboard/dashboard.html')


@admin_login_required
@generate_pagination
def users():
    return render_template('admin/users/users.html',
                           modify_user_form=ModifyUserForm(),
                           add_user_form=AddUserForm(),
                           search_form=SearchForm(),
                           # bulk_delete_form=BulkDeleteForm(),
                           item_pagination=g.item_pagination)


@admin_login_required
@generate_pagination
def admin_users():
    return render_template('admin/admin_users/admin_users.html',
                           modify_admin_user_form=ModifyAdminUserForm(),
                           add_admin_user_form=AddAdminUserForm(),
                           search_form=SearchForm(),
                           item_pagination=g.item_pagination)


@admin_login_required
@generate_pagination
def roles():
    return render_template('admin/roles/roles.html',
                           modify_role_form=ModifyRoleForm(),
                           add_role_form=AddRoleForm(),
                           search_form=SearchForm(),
                           item_pagination=g.item_pagination)


@admin_login_required
@generate_pagination
def admin_roles():
    return render_template('admin/admin_roles/admin_roles.html',
                           modify_admin_role_form=ModifyAdminRoleForm(),
                           add_admin_role_form=AddAdminRoleForm(),
                           search_form=SearchForm(),
                           item_pagination=g.item_pagination)


@admin_login_required
@generate_pagination
def faq():
    return render_template('admin/faq/faq.html',
                           faq_form=ModifyFAQForm(),
                           new_faq_form=AddFAQForm())


@admin_login_required
def content_home_page():
    return render_template('admin/content/home_page/home_page.html',
                           quill_html_form=ContentDraftTextForm(),
                           quill_image_form=ContentDraftImageForm(),
                           content_publish_form=ContentPublishForm())


@admin_login_required
def content_about_page():
    return render_template('admin/content/about_page/about_page.html',
                           quill_html_form=ContentDraftTextForm(),
                           quill_image_form=ContentDraftImageForm(),
                           content_publish_form=ContentPublishForm())


@admin_login_required
def content_contact_page():
    return render_template('admin/content/contact_page/contact_page.html',
                           quill_html_form=ContentDraftTextForm(),
                           quill_image_form=ContentDraftImageForm(),
                           content_publish_form=ContentPublishForm())


@admin_login_required
def content_image(field_name, image_id):
    filename = '{}.jpg'.format(image_id.lower())
    file_path = path.join(current_app.config['CONTENT_IMAGE_UPLOAD_PATH'], field_name.upper())
    return send_from_directory(directory=file_path, filename=filename)
