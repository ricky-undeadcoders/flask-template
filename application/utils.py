#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import current_app, render_template, g
from flask_mail import Message
from flask_security.utils import config_value


def send_mail(subject, recipients, template, **context):
    current_app.logger.debug('Sending email "{}" to\n{}'.format(subject, recipients))
    mail = current_app.extensions.get('mail')
    message = Message(subject=subject,
                      sender=current_app.config['MAIL_DEFAULT_SENDER'],
                      recipients=recipients)
    ctx = ('email', template)

    if config_value('EMAIL_PLAINTEXT'):
        message.body = render_template('{}/{}.txt'.format(*ctx), **context)
    if config_value('EMAIL_HTML'):
        message.html = render_template('{}/{}.html'.format(*ctx), **context)

    if current_app.testing is False:
        mail.send(message)
        current_app.logger.info('Email sent!')
