#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import (current_app, g, request, url_for, render_template)
from collections import OrderedDict
from wtforms import (SubmitField,
                     StringField,
                     BooleanField,
                     IntegerField,
                     SelectField,
                     HiddenField)
from wtforms.validators import (DataRequired, Email, Length, Regexp)
from base64 import decodestring

from application.forms import CustomForm
from application.config import datastore_config as ds_config
from application.middleware import remove_whitespace


class AddUserForm(CustomForm):
    username = StringField(validators=[DataRequired(),
                                       Length(max=ds_config.USER_USERNAME_MAX_LENGTH),
                                       Regexp(regex=ds_config.USER_USERNAME_REGEX)])
    first_name = StringField(validators=[Length(max=ds_config.USER_FIRST_NAME_MAX_LENGTH),
                                         Regexp(regex=ds_config.USER_FIRST_NAME_REGEX)])
    last_name = StringField(validators=[Length(max=ds_config.USER_LAST_NAME_MAX_LENGTH),
                                        Regexp(regex=ds_config.USER_LAST_NAME_REGEX)])
    email = StringField(validators=[DataRequired(),
                                    Length(max=ds_config.USER_EMAIL_MAX_LENGTH),
                                    Email()])

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = 'Created User!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        if self.username.data:
            username_user = g.datastore.find_user(username=self.username.data)
            if username_user:
                self.username.errors.append(current_app.config['MSG_USERNAME_CLAIMED'])
                return self.validation_error()
        if self.email.data:
            email_user = g.datastore.find_user(email=self.email.data)
            if email_user:
                self.email.errors.append(current_app.config['MSG_EMAIL_CLAIMED'])
                return self.validation_error()
        self.kwargs.update({'username': self.username.data})
        self.kwargs.update({'first_name': self.first_name.data})
        self.kwargs.update({'last_name': self.last_name.data})
        self.kwargs.update({'email': self.email.data})
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to create admin user: {}'.format(self.username.data))
        user = g.datastore.create_user(**self.kwargs)
        if user:
            current_app.logger.info('Successfully created user')
            return self.update_success()
        else:
            current_app.logger.error('Failure creating user')
            return self.update_error()


class AddAdminUserForm(CustomForm):
    username = StringField(validators=[DataRequired(),
                                       Length(max=ds_config.USER_USERNAME_MAX_LENGTH),
                                       Regexp(regex=ds_config.USER_USERNAME_REGEX)])
    first_name = StringField(validators=[Length(max=ds_config.USER_FIRST_NAME_MAX_LENGTH),
                                         Regexp(regex=ds_config.USER_FIRST_NAME_REGEX)])
    last_name = StringField(validators=[Length(max=ds_config.USER_LAST_NAME_MAX_LENGTH),
                                        Regexp(regex=ds_config.USER_LAST_NAME_REGEX)])
    email = StringField(validators=[DataRequired(),
                                    Length(max=ds_config.USER_EMAIL_MAX_LENGTH),
                                    Email()])
    bio = StringField()

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = 'Created Admin User!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        if self.username.data:
            username_user = g.datastore.find_user(username=self.username.data)
            if username_user:
                self.username.errors.append(current_app.config['MSG_USERNAME_CLAIMED'])
                return self.validation_error()
        if self.email.data:
            email_user = g.datastore.find_user(email=self.email.data)
            if email_user:
                self.email.errors.append(current_app.config['MSG_EMAIL_CLAIMED'])
                return self.validation_error()
        self.kwargs.update({'username': self.username.data})
        self.kwargs.update({'first_name': self.first_name.data})
        self.kwargs.update({'last_name': self.last_name.data})
        self.kwargs.update({'email': self.email.data})
        self.kwargs.update({'bio': self.bio.data})
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to create admin user: {}'.format(self.username.data))
        user = g.datastore.create_admin_user(**self.kwargs)
        if user:
            current_app.logger.info('Successfully created admin user')
            return self.update_success()
        else:
            current_app.logger.error('Failure creating admin user')
            return self.update_error()


class ModifyUserForm(CustomForm):
    user_id = StringField(validators=[DataRequired()])
    reset_password = BooleanField()
    username = StringField(validators=[Length(max=ds_config.USER_USERNAME_MAX_LENGTH),
                                       Regexp(regex=ds_config.USER_USERNAME_REGEX)])
    first_name = StringField(validators=[Length(max=ds_config.USER_FIRST_NAME_MAX_LENGTH),
                                         Regexp(regex=ds_config.USER_FIRST_NAME_REGEX)])
    last_name = StringField(validators=[Length(max=ds_config.USER_LAST_NAME_MAX_LENGTH),
                                        Regexp(regex=ds_config.USER_LAST_NAME_REGEX)])
    email = StringField(validators=[Length(max=ds_config.USER_EMAIL_MAX_LENGTH)])
    bio = StringField(validators=[Length(max=ds_config.USER_BIO_MAX_LENGTH)])
    active = StringField()
    roles = StringField()

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = 'Updated user!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.user = g.datastore.find_user(id=self.user_id.data)
        if not self.user:
            self.user_id.errors.append('Invalid User')
            return self.validation_error()
        if self.username.data:
            username_user = g.datastore.find_user(username=self.username.data)
            if username_user and username_user.id != self.user.id:
                self.username.errors.append(current_app.config['MSG_USERNAME_CLAIMED'])
                return self.validation_error()
        if self.email.data:
            email_user = g.datastore.find_user(email=self.email.data)
            if email_user and email_user.id != self.user.id:
                self.email.errors.append(current_app.config['MSG_EMAIL_CLAIMED'])
                return self.validation_error()

        if self.first_name.data != self.user.first_name:
            self.kwargs.update({'first_name': self.first_name.data})
        if self.last_name.data != self.user.last_name:
            self.kwargs.update({'last_name': self.last_name.data})
        if self.username.data != self.user.username:
            self.kwargs.update({'username': self.username.data})
        if self.email.data != self.user.email:
            self.kwargs.update({'email': self.email.data})
        if self.bio.data != self.user.bio:
            self.kwargs.update({'bio': self.bio.data})
        if self.active.data == 'on':
            active = True
        else:
            active = False
        if active != self.user.active:
            self.toggle_active = True
        if self.roles.data:
            role_list = []
            for role in self.roles.data.strip(',').split(','):
                role_obj = g.datastore.find_role(name=role)
                if role_obj:
                    role_list.append(role_obj)
            if role_list != self.user.roles:
                self.kwargs.update({'roles': role_list})
        if len(self.kwargs) == 0 and self.toggle_active is False:
            self.user_id.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()

        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to update user: {}'.format(self.user_id.data))
        if self.toggle_active:
            toggled = g.datastore.toggle_active(self.user)
        user = g.datastore.modify_user(user=self.user, **self.kwargs)
        if user:
            current_app.logger.info('Successfully updated user')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating user')
            return self.update_error()

    def update_success(self):
        self.render_html.update({'user_html': render_template(
            'admin/users/user_list_collapse_row.html',
            chevron='fa fa-chevron-down',
            user=self.user)})
        return CustomForm.update_success(self)


class ModifyAdminUserForm(CustomForm):
    user_id = StringField(validators=[DataRequired()])
    reset_password = BooleanField()
    username = StringField(validators=[Length(max=ds_config.USER_USERNAME_MAX_LENGTH),
                                       Regexp(regex=ds_config.USER_USERNAME_REGEX)])
    first_name = StringField(validators=[Length(max=ds_config.USER_FIRST_NAME_MAX_LENGTH),
                                         Regexp(regex=ds_config.USER_FIRST_NAME_REGEX)])
    last_name = StringField(validators=[Length(max=ds_config.USER_LAST_NAME_MAX_LENGTH),
                                        Regexp(regex=ds_config.USER_LAST_NAME_REGEX)])
    email = StringField(validators=[Length(max=ds_config.USER_EMAIL_MAX_LENGTH)])
    active = StringField()
    roles = StringField()
    bio = StringField(validators=[Length(max=ds_config.USER_BIO_MAX_LENGTH)])

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.user = None
        self.success_message = 'Updated user!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.user = g.datastore.find_user(id=self.user_id.data)
        if not self.user:
            self.user_id.errors.append('Invalid User')
            return self.validation_error()
        if self.username.data:
            username_user = g.datastore.find_user(username=self.username.data)
            if username_user and username_user.id != self.user.id:
                self.username.errors.append('This username has already been claimed')
                return self.validation_error()
        if self.email.data:
            email_user = g.datastore.find_user(email=self.email.data)
            if email_user and email_user.id != self.user.id:
                self.email.errors.append(current_app.config['MSG_EMAIL_CLAIMED'])
                return self.validation_error()

        if self.first_name.data != self.user.first_name:
            self.kwargs.update({'first_name': self.first_name.data})
        if self.last_name.data != self.user.last_name:
            self.kwargs.update({'last_name': self.last_name.data})
        if self.username.data != self.user.username:
            self.kwargs.update({'username': self.username.data})
        if self.email.data != self.user.email:
            self.kwargs.update({'email': self.email.data})
        if self.bio.data != self.user.bio:
            self.kwargs.update({'bio': self.bio.data})
        if self.active.data == 'on':
            active = True
        else:
            active = False
        if active != self.user.active:
            self.toggle_active = True
        if self.roles.data:
            role_list = []
            for role in self.roles.data.strip(',').split(','):
                role_obj = g.datastore.find_admin_role(name=role)
                if role_obj:
                    role_list.append(role_obj)
            if role_list != self.user.roles:
                self.kwargs.update({'roles': role_list})
        if len(self.kwargs) == 0 and self.toggle_active is False:
            self.user_id.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()

        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to update admin user: {}'.format(self.user_id.data))
        if self.toggle_active:
            toggled = g.datastore.toggle_active(self.user)
        user = g.datastore.modify_admin_user(user=self.user, **self.kwargs)
        if user:
            current_app.logger.info('Successfully updated user')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating user')
            return self.update_error()

    def update_success(self):
        self.render_html.update({'admin_users_html': render_template(
            'admin/admin_users/admin_users_list_collapse_row.html',
            chevron='fa fa-chevron-down',
            admin_user=self.user)})
        return CustomForm.update_success(self)


class AddRoleForm(CustomForm):
    name = StringField(validators=[DataRequired(),
                                   Length(max=ds_config.ROLE_NAME_MAX_LENGTH),
                                   Regexp(regex=ds_config.ROLE_NAME_REGEX)])
    description = StringField(validators=[Length(max=ds_config.ROLE_DESCRIPTION_MAX_LENGTH),
                                          Regexp(regex=ds_config.ROLE_DESCRIPTION_REGEX)])

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.role = None
        self.success_message = 'Created Role!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        if self.name.data:
            name_role = g.datastore.find_role(name=self.name.data)
            if name_role:
                self.name.errors.append(current_app.config['MSG_ROLE_EXISTS'])
                return self.validation_error()
        self.kwargs.update({'name': self.name.data})
        self.kwargs.update({'description': self.description.data})
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to create role: {}'.format(self.name.data))
        role = g.datastore.create_role(**self.kwargs)
        if role:
            current_app.logger.info('Successfully created role')
            return self.update_success()
        else:
            current_app.logger.error('Failure creating role')
            return self.update_error()


class ModifyRoleForm(CustomForm):
    role_id = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired(),
                                   Length(max=ds_config.ROLE_NAME_MAX_LENGTH),
                                   Regexp(regex=ds_config.ROLE_NAME_REGEX)])
    description = StringField(validators=[Length(max=ds_config.ROLE_DESCRIPTION_MAX_LENGTH),
                                          Regexp(regex=ds_config.ROLE_DESCRIPTION_REGEX)])
    active = StringField()

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.role = None
        self.success_message = 'Updated Role!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.role = g.datastore.find_role(id=self.role_id.data)
        if not self.role:
            self.role_id.errors.append('Invalid Role')
            return self.validation_error()

        if self.name.data != self.role.name:
            self.kwargs.update({'name': self.name.data})
        if self.description.data != self.role.description:
            self.kwargs.update({'description': self.description.data})
        if self.active.data == 'on':
            active = True
        else:
            active = False
        if active != self.role.active:
            self.toggle_active = True
        if len(self.kwargs) == 0 and self.toggle_active is False:
            self.role_id.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()

        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to update role: {}'.format(self.role_id.data))
        if self.toggle_active:
            toggled = g.datastore.toggle_active(self.role)
        role = g.datastore.modify_role(role=self.role, **self.kwargs)
        if role:
            current_app.logger.info('Successfully updated role')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating role')
            return self.update_error()

    def update_success(self):
        self.render_html.update({'role_html': render_template(
            'admin/roles/role_list_collapse_row.html',
            chevron='fa fa-chevron-down',
            role=self.role)})
        return CustomForm.update_success(self)


class AddAdminRoleForm(CustomForm):
    name = StringField(validators=[DataRequired(),
                                   Length(max=ds_config.ROLE_NAME_MAX_LENGTH),
                                   Regexp(regex=ds_config.ROLE_NAME_REGEX)])
    description = StringField(validators=[Length(max=ds_config.ROLE_DESCRIPTION_MAX_LENGTH),
                                          Regexp(regex=ds_config.ROLE_DESCRIPTION_REGEX)])

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.role = None
        self.success_message = 'Created Admin Role!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        if self.name.data:
            name_role = g.datastore.find_admin_role(name=self.name.data)
            if name_role:
                self.name.errors.append(current_app.config['MSG_ROLE_EXISTS'])
                return self.validation_error()
        self.kwargs.update({'name': self.name.data})
        self.kwargs.update({'description': self.description.data})
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to create role: {}'.format(self.name.data))
        role = g.datastore.create_admin_role(**self.kwargs)
        if role:
            current_app.logger.info('Successfully created admin role')
            return self.update_success()
        else:
            current_app.logger.error('Failure creating admin role')
            return self.update_error()


class ModifyAdminRoleForm(CustomForm):
    admin_role_id = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired(),
                                   Length(max=ds_config.ROLE_NAME_MAX_LENGTH),
                                   Regexp(regex=ds_config.ROLE_NAME_REGEX)])
    description = StringField(validators=[Length(max=ds_config.ROLE_DESCRIPTION_MAX_LENGTH),
                                          Regexp(regex=ds_config.ROLE_DESCRIPTION_REGEX)])
    active = StringField()

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.role = None
        self.success_message = 'Updated Admin Role!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.role = g.datastore.find_admin_role(id=self.admin_role_id.data)
        if not self.role:
            self.admin_role_id.errors.append('Invalid Admin Role')
            return self.validation_error()

        if self.name.data != self.role.name:
            self.kwargs.update({'name': self.name.data})
        if self.description.data != self.role.description:
            self.kwargs.update({'description': self.description.data})
        if self.active.data == 'on':
            active = True
        else:
            active = False
        if active != self.role.active:
            self.toggle_active = True
        if len(self.kwargs) == 0 and self.toggle_active is False:
            self.admin_role_id.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()

        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to update role: {}'.format(self.admin_role_id.data))
        if self.toggle_active:
            toggled = g.datastore.toggle_active(self.role)
        role = g.datastore.modify_role(role=self.role, **self.kwargs)
        if role:
            current_app.logger.info('Successfully updated role')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating role')
            return self.update_error()

    def update_success(self):
        self.render_html.update({'admin_role_html': render_template(
            'admin/admin_roles/admin_role_list_collapse_row.html',
            chevron='fa fa-chevron-down',
            admin_role=self.role)})
        return CustomForm.update_success(self)


class AddFAQForm(CustomForm):
    order = IntegerField(validators=[DataRequired()])
    question = StringField(validators=[DataRequired(),
                                       Length(max=ds_config.FAQ_QUESTION_MAX_LENGTH)])
    answer = StringField(validators=[DataRequired(),
                                     Length(max=ds_config.FAQ_ANSWER_MAX_LENGTH)])

    def __init__(self, *args, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.role = None
        self.success_message = 'Created FAQ!'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        if g.datastore.find_faq(order=self.order.data):
            self.order.errors.append('That FAQ order is already assigned')
            return self.validation_error()
        self.kwargs.update({'order': self.order.data})
        self.kwargs.update({'question': self.question.data})
        self.kwargs.update({'answer': self.answer.data})
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to create faq')
        faq = g.datastore.create_faq(**self.kwargs)
        if faq:
            current_app.logger.info('Successfully created FAQ')
            return self.update_success()
        else:
            current_app.logger.error('Failure creating FAQ')
            return self.update_error()


class ModifyFAQForm(CustomForm):
    faq_id = HiddenField()
    order = IntegerField(validators=[DataRequired()])
    question = StringField(validators=[DataRequired(),
                                       Length(max=ds_config.FAQ_QUESTION_MAX_LENGTH)])
    answer = StringField(validators=[DataRequired(),
                                     Length(max=ds_config.FAQ_ANSWER_MAX_LENGTH)])
    active = StringField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.success_message = 'Updated FAQ!'
        self.faq = None

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.faq = g.datastore.find_faq(id=self.faq_id.data)
        if not self.faq:
            self.faq_id.errors.append('Invalid FAQ')
            return self.validation_error()
        if self.order.data != self.faq.order:
            if g.datastore.find_faq(order=self.order.data):
                self.order.errors.append('That FAQ order is already assigned')
                return self.validation_error()
            self.kwargs.update({'order': self.order.data})
        if self.question.data != self.faq.question:
            self.kwargs.update({'question': self.question.data})
        if self.answer.data != self.faq.answer:
            self.kwargs.update({'answer': self.answer.data})
        if self.active.data == 'on':
            active = True
        else:
            active = False
        if active != self.faq.active:
            self.toggle_active = True
        if len(self.kwargs) == 0 and self.toggle_active is False:
            self.faq_id.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            self.update_error()
        current_app.logger.info('Attempting to update faq: {}'.format(self.faq_id.data))
        if self.toggle_active:
            toggled = g.datastore.toggle_active(self.faq)
        self.faq = g.datastore.modify_faq(faq=self.faq, **self.kwargs)
        if self.faq:
            current_app.logger.info('Successfully updated faq')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating faq')
            return self.update_error()

    def update_success(self):
        self.render_html.update({'faq_html': render_template(
            'admin/faq/faq_list_collapse_row.html',
            chevron='fa fa-chevron-down',
            faq=self.faq)})
        return CustomForm.update_success(self)


class ContentDraftTextForm(CustomForm):
    field_name = HiddenField(validators=[DataRequired()])
    content_text = HiddenField(validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.content = None
        self.success_message = 'Content Draft Updated'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.content = g.datastore.find_content(field_name=self.field_name.data, draft=True)
        if not self.content:
            self.field_name.errors.append(current_app.config['GENERIC_FORM_ERROR_MESSAGE'])
            return self.validation_error()
        if remove_whitespace(self.content_text.data) != remove_whitespace(self.content.text):
            self.kwargs.update({'text': remove_whitespace(self.content_text.data)})
        if len(self.kwargs) == 0:
            self.content_text.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            return self.validation_error()
        current_app.logger.info('Attempting to update content draft text: {}'.format(self.field_name.data))
        data = g.datastore.modify_content_draft(content=self.content,
                                                text=remove_whitespace(self.content_text.data))
        if data:
            current_app.logger.info('Successfully updated content draft data')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating content draft data: {}'.format(data))
            return self.update_error()

    def update_success(self):
        self.render_html['content_html'] = self.content.text
        return CustomForm.update_success(self)


class ContentDraftImageForm(CustomForm):
    field_name = HiddenField(validators=[DataRequired()])
    image_id = HiddenField(validators=[DataRequired()])
    image = HiddenField(validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.render_html = None

    def validate_on_submit(self):
        self.submit.data = True  # TODO: remove this (means we need to have it submit via the form button, or set it via JS)
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        try:
            decodestring(self.image.data)
        except Exception, e:
            current_app.logger.error('String was not valid base64: {}'.format(e))
            self.image_id.errors.append(current_app.config['GENERIC_FORM_ERROR_MESSAGE'])
            return self.validation_error()
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            return self.update_error()
        current_app.logger.info('Attempting to upload quill image: {}'.format(self.image_id.data))

        # upload_pic = UploadImage(image=self.image.data,
        #                          upload_path=current_app.config['QUILL_IMAGE_UPLOAD_PATH'],
        #                          image_specs=current_app.config['QUILL_IMAGE_SPECS'],
        #                          subfolder_name=self.field_name.data,
        #                          image_name=str(self.image_id.data),
        #                          encoding='base64')
        success, data = upload_pic.resize_and_save_image()
        if success:
            current_app.logger.info('Successfully uploaded quill image')
            return self.update_success()
        else:
            current_app.logger.error('Failure uploading quill image: {}'.format(data))
            self.append_error_with_field_name(field_name=data.field_name, message=data)
            return self.update_error()


class ContentPublishForm(CustomForm):
    field_name = HiddenField(validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)
        self.content = None
        self.content_draft = None
        self.success_message = 'Content Published'

    def validate_on_submit(self):
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.content = g.datastore.find_content(field_name=self.field_name.data)
        if not self.content:
            current_app.logger.error('Unable to resolve content')
            self.field_name.errors.append(current_app.config['GENERIC_FORM_ERROR_MESSAGE'])
            return self.validation_error()
        self.content_draft = g.datastore.find_content(field_name=self.field_name.data, draft=True)
        if not self.content:
            current_app.logger.error('Unable to resolve content draft')
            self.field_name.errors.append(current_app.config['GENERIC_FORM_ERROR_MESSAGE'])
            return self.validation_error()
        if remove_whitespace(self.content.text) != remove_whitespace(self.content_draft.text):
            self.kwargs.update({'update_text': True})
        if len(self.kwargs) == 0:
            self.field_name.errors.append(current_app.config['NO_DATA_CHANGED'])
            return self.validation_error()
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            return self.validation_error()
        current_app.logger.info('Attempting to publish content: {}'.format(self.field_name.data))
        data = g.datastore.publish_content(content=self.content,
                                           content_draft=self.content_draft)
        if data:
            current_app.logger.info('Successfully published content')
            return self.update_success()
        else:
            current_app.logger.error('Failure publishing content: {}'.format(data))
            return self.update_error()

    def update_success(self):
        self.render_html['content_html'] = self.content.text
        return CustomForm.update_success(self)


class SearchForm(CustomForm):
    q = StringField(validators=[DataRequired()])


class BulkDeleteForm(CustomForm):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField(validators=[DataRequired()],
                        choices=['All selected items',
                                 'All search results'])
