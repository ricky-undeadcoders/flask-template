#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import g, current_app, render_template
from flask_security import current_user
from wtforms import (StringField, IntegerField, BooleanField)
from wtforms.validators import (Length,
                                DataRequired)

from application.forms import CustomForm
from application.config import datastore_config as ds_config
from application.middleware import remove_whitespace


class AddPostForm(CustomForm):
    title = StringField(validators=[Length(max=ds_config.POST_TITLE_MAX_LENGTH)])
    body = StringField(validators=[Length(max=ds_config.POST_BODY_MAX_LENGTH)])

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = 'Post Created!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.kwargs.update({'title': remove_whitespace(self.title.data)})
        self.kwargs.update({'body': remove_whitespace(self.body.data)})
        self.kwargs.update({'user': current_user})
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to create post')
        post = g.datastore.create_post(**self.kwargs)
        if post:
            current_app.logger.info('Successfully created post')
            return self.update_success()
        else:
            current_app.logger.error('Failure creating post')
            return self.update_error()


class ModifyPostForm(CustomForm):
    post_id = IntegerField(validators=[DataRequired()])
    # user_id = IntegerField()
    title = StringField(validators=[Length(max=ds_config.POST_TITLE_MAX_LENGTH)])
    body = StringField(validators=[Length(max=ds_config.POST_BODY_MAX_LENGTH)])
    active = BooleanField()

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.post = None
        self.user = None
        self.success_message = 'Post Updated!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.post = g.datastore.find_post(id=self.post_id.data)
        if not self.post:
            self.post_id.errors.append('Invalid post')
            return self.validation_error()
        if self.title.data != self.post.title:
            self.kwargs.update({'title': remove_whitespace(self.title.data)})
        if self.body.data != self.post.body:
            self.kwargs.update({'body': remove_whitespace(self.body.data)})
        if self.active.data != self.post.active:
            g.datastore.toggle_active(self.post)
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to create post')
        post = g.datastore.modify_post(post=self.post, **self.kwargs)
        if post:
            current_app.logger.info('Successfully created post')
            return self.update_success()
        else:
            current_app.logger.error('Failure creating post')
            return self.update_error()

    def update_success(self):
        self.render_html.update({'post_html': render_template(
            'blog/admin/post_list_collapse_row.html',
            chevron='fa fa-chevron-down',
            post=self.post)})
        return CustomForm.update_success(self)
