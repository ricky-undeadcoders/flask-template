#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint

from application.bp.login.views_html import (login,
                                             logout,
                                             user_settings,
                                             register,
                                             confirm_email,
                                             forgot_password,
                                             reset_password,
                                             resend_confirmation_email,
                                             confirm_email_modification)
from application.bp.login.views_json import (user_settings_change_password,
                                             user_settings_change_name,
                                             user_settings_change_username,
                                             modify_and_confirm_email,
                                             forgot_password_exec)

blueprint = Blueprint(name='login',
                      import_name=__name__)
blueprint.__version__ = '1.0.0'

##############################################
# HTML RULES
##############################################
blueprint.add_url_rule('/login/', 'login', login, methods=['GET', 'POST'])
blueprint.add_url_rule('/logout/', 'logout', logout, methods=['GET'])
blueprint.add_url_rule('/user-settings/', 'user_settings', user_settings, methods=['GET'])
blueprint.add_url_rule('/register/', 'register', register, methods=['GET', 'POST'])
blueprint.add_url_rule('/confirm-email/<token>', 'confirm_email', confirm_email, methods=['GET'])
blueprint.add_url_rule('/confirm-email-modification/<token>', 'confirm_email_modification', confirm_email_modification,
                       methods=['GET'])
blueprint.add_url_rule('/forgot-password/', 'forgot_password', forgot_password, methods=['GET'])
blueprint.add_url_rule('/reset-password/<token>', 'reset_password', reset_password, methods=['GET', 'POST'])
blueprint.add_url_rule('/resend-confirmation-email/', 'resend_confirmation_email', resend_confirmation_email,
                       methods=['GET', 'POST'])

##############################################
# JSON RULES
##############################################
blueprint.add_url_rule('/user-settings-change-password/', 'user_settings_change_password',
                       user_settings_change_password, methods=['POST'])
blueprint.add_url_rule('/user-settings-change-name/', 'user_settings_change_name', user_settings_change_name,
                       methods=['POST'])
blueprint.add_url_rule('/user-settings-change-username/', 'user_settings_change_username',
                       user_settings_change_username, methods=['POST'])
blueprint.add_url_rule('/modify-and-confirm-email/', 'modify_and_confirm_email', modify_and_confirm_email,
                       methods=['POST'])
blueprint.add_url_rule('/forgot-password-exec/', 'forgot_password_exec', forgot_password_exec, methods=['POST'])
