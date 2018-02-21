#!/usr/bin/python3
# -*- coding: utf-8 -*-

from application.bp.login.forms import LoginForm

###################################################
# FLASK LOGIN MANAGER SETTINGS
# Set your redirects for
# unauthorized users per blueprint
###################################################
BLUEPRINT_LOGIN_VIEWS = {'admin': 'admin.login',
                         'login': 'login.login',
                         'main': 'login.login'}

LOGIN_FORM = LoginForm

###################################################
# SQLALCHEMY
# This can track db mods for a huge memory price
###################################################
SQLALCHEMY_TRACK_MODIFICATIONS = False

###################################################
# FLASK-SECURITY SETTINGS
# https://pythonhosted.org/Flask-Security/configuration.html
###################################################
SECURITY_TRACKABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = True
SECURITY_UNAUTHORIZED_VIEW = 'login.login'
SECURITY_MSG_UNAUTHORIZED = ('Please log in to view this page', 'error')
SECURITY_RESET_URL = 'login.reset_password'
SECURITY_PASSWORD_HASH = 'sha512_crypt'

###################################################
# IMAGE UPLOAD CONFIGURATIONS
###################################################
CONTENT_IMAGE_UPLOAD_PATH = '/uploads/content'

###################################################
# BLUEPRINTS TO INCLUDE IN SITE MAP
###################################################
SITE_MAP_BLUEPRINTS = ['main']

###################################################
# GLOBAL MAIL SETTINGS
###################################################
MAIL_DEFAULT_SENDER = 'info@undeadcodersociety.com'

###################################################
# RECAPTCHA ACCT
###################################################
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

###################################################
# OTHER CONFIGS
###################################################
ERROR_MESSAGE_TTL = 5000
REGISTRATION_BY_INVITE_ONLY = True


