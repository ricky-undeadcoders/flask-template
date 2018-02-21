#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import (current_app, g, flash, get_flashed_messages)
from flask_wtf import FlaskForm


class CustomForm(FlaskForm):
    def __init__(self, **kwargs):
        self.validated = False
        self.success_message = None
        self.toggle_active = False
        self.render_html = {}
        self.kwargs = {}
        FlaskForm.__init__(self, **kwargs)

    def validation_success(self):
        self.validated = True
        current_app.logger.info('Form validated successfully')
        return True

    def validation_error(self):
        print self.errors
        if len(self.errors) > 0:
            print 'where we should be'
            flash(self.errors, 'error')
        # current_app.logger.error('Form did not validate: {}'.format(get_flashed_messages(category_filter='error')))
        return False

    def update_success(self):
        flash(self.success_message, 'success')
        current_app.logger.info('Successfully updated form data')
        return True

    def update_error(self):
        current_app.logger.error('Form did not update: {}'.format(get_flashed_messages(category_filter='error')))
        return False

    def validate_on_submit(self):
        current_app.logger.debug('Validating data: {}'.format(self.data))
        valid = True
        if not FlaskForm.validate_on_submit(self):
            valid = False
            current_app.logger.error('Validity check failed on FlaskForm fields')
        return valid

    def append_error_with_field_name(self, field_name, message):
        if not self.errors.get(field_name):
            self.errors[field_name] = []
        self.errors[field_name].append(str(message))
