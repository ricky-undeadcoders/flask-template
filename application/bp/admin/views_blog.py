# !/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import (current_app, flash, redirect, url_for, render_template, g, jsonify, get_flashed_messages)

from application.login_decorators import admin_login_required
from application.bp.admin.decorators import generate_pagination
from application.bp.blog.forms import AddPostForm, ModifyPostForm
from application.bp.admin.forms import SearchForm


@admin_login_required
@generate_pagination
def blog():
    return render_template('blog/admin/blog.html',
                           add_post_form=AddPostForm(),
                           modify_post_form=ModifyPostForm(),
                           search_form=SearchForm(),
                           item_pagination=g.item_pagination)


@admin_login_required
def post(post_id):
    try:
        post = g.datastore.find_post(id=post_id)
        if post:
            return render_template('blog/admin/post.html',
                                   post=post,
                                   post_form=ModifyPostForm())
    except Exception, e:
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')
        current_app.logger.error('Fatal error attempting to add user; error: {}'.format(e))
    return redirect('admin.blog')


@admin_login_required
def add_post():
    try:
        form = AddPostForm()
        if form.validate_on_submit():
            if form.update_data():
                current_app.logger.info('Successfully added post')
    except Exception, e:
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')
        current_app.logger.error('Fatal error attempting to add user; error: {}'.format(e))

    return redirect(url_for('admin.blog'))


@admin_login_required
def modify_post():
    try:
        form = ModifyPostForm()
        if form.validate_on_submit():
            if form.update_data():
                return jsonify({'message': get_flashed_messages(category_filter='success'),
                                'render_html': form.render_html
                                }), 200, {}
    except Exception, e:
        current_app.logger.error('Fatal error attempting to modify post; error: {}'.format(e))
        flash(current_app.config['GENERIC_FORM_ERROR_MESSAGE'], 'error')

    return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}
