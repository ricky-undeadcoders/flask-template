#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import g
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     SubmitField,
                     HiddenField,
                     SelectField,
                     SelectMultipleField)
from wtforms.validators import Email, DataRequired, URL


class SubscriptionForm(FlaskForm):
    email = StringField(label='Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField(label='Subscribe')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate_on_submit(self):
        if not FlaskForm.validate_on_submit(self):
            return False
        print self.email.data.lower()
        contact_email = g.datastore.find_subscription_email(email=self.email.data.lower())
        print contact_email
        if contact_email:
            self.email.errors.append('This email has already been registered')
            return False
        return True


class ContactUsForm(FlaskForm):
    contact_email = StringField(validators=[DataRequired(), Email()])
    contact_message = StringField(validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, **kwargs):
        FlaskForm.__init__(self, **kwargs)

    def validate_on_submit(self):
        if not FlaskForm.validate_on_submit(self):
            return False
        return True
