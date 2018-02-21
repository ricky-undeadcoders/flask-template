#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint
from application.bp.admin.views_json import (modify_user,
                                             modify_admin_user,
                                             add_admin_user,
                                             add_user,
                                             add_role,
                                             modify_role,
                                             add_admin_role,
                                             modify_admin_role,
                                             modify_content,
                                             upload_content_image,
                                             publish_content,
                                             user_settings_change_password,
                                             add_faq,
                                             modify_faq)
from application.bp.admin.views_html import (login,
                                             logout,
                                             user_settings,
                                             dashboard,
                                             users,
                                             admin_users,
                                             roles,
                                             admin_roles,
                                             content_home_page,
                                             content_about_page,
                                             content_contact_page,
                                             content_image,
                                             faq)

blueprint = Blueprint(name='admin',
                      import_name=__name__,
                      url_prefix='/admin')
blueprint.__version__ = '1.0.0'

##############################################
# HTML RULES
##############################################
blueprint.add_url_rule('/login/', 'login', login, methods=['GET', 'POST'])
# blueprint.add_url_rule('/logout/', 'logout', logout, methods=['GET'])
blueprint.add_url_rule('/user-settings/', 'user_settings', user_settings, methods=['GET'])
blueprint.add_url_rule('/', 'dashboard', dashboard, methods=['GET'])
blueprint.add_url_rule('/users/', 'users', users, methods=['GET'])
blueprint.add_url_rule('/admin-users/', 'admin_users', admin_users, methods=['GET'])
blueprint.add_url_rule('/roles/', 'roles', roles, methods=['GET'])
blueprint.add_url_rule('/faq/', 'faq', faq, methods=['GET'])
blueprint.add_url_rule('/admin-roles/', 'admin_roles', admin_roles, methods=['GET'])
blueprint.add_url_rule('/content/home/', 'content_home_page', content_home_page, methods=['GET'])
blueprint.add_url_rule('/content/about/', 'content_about_page', content_about_page, methods=['GET'])
blueprint.add_url_rule('/content/contact/', 'content_contact_page', content_contact_page, methods=['GET'])
blueprint.add_url_rule('/content-image/<string:field_name>/<string:image_id>/', 'content_image', content_image,
                       methods=['GET'])

##############################################
# JSON RULES
##############################################
blueprint.add_url_rule('/user-settings-change-password/', 'user_settings_change_password', user_settings_change_password, methods=['POST'])
blueprint.add_url_rule('/add-user/', 'add_user', add_user, methods=['POST'])
blueprint.add_url_rule('/modify-user/', 'modify_user', modify_user, methods=['POST'])
blueprint.add_url_rule('/add-admin-user/', 'add_admin_user', add_admin_user, methods=['POST'])
blueprint.add_url_rule('/modify-admin-user/', 'modify_admin_user', modify_admin_user, methods=['POST'])
blueprint.add_url_rule('/add-role/', 'add_role', add_role, methods=['POST'])
blueprint.add_url_rule('/add-admin-role/', 'add_admin_role', add_admin_role, methods=['POST'])
blueprint.add_url_rule('/add-faq/', 'add_faq', add_faq, methods=['POST'])
blueprint.add_url_rule('/modify-role/', 'modify_role', modify_role, methods=['POST'])
blueprint.add_url_rule('/modify-admin-role/', 'modify_admin_role', modify_admin_role, methods=['POST'])
blueprint.add_url_rule('/modify-faq/', 'modify_faq', modify_faq, methods=['POST'])
blueprint.add_url_rule('/modify-content/', 'modify_content', modify_content, methods=['POST'])
blueprint.add_url_rule('/upload-content-image/', 'upload_content_image', upload_content_image, methods=['POST'])
blueprint.add_url_rule('/publish-content/', 'publish_content', publish_content, methods=['POST'])


##############################################
# BLOG RULES
##############################################
from application.bp.admin.views_blog import blog, post, add_post, modify_post
blueprint.add_url_rule('/blog/', 'blog', blog, methods=['GET'])
blueprint.add_url_rule('/post/<int:post_id>/', 'post', post, methods=['GET'])
blueprint.add_url_rule('/add-post/', 'add_post', add_post, methods=['POST'])
blueprint.add_url_rule('/modify-post/', 'modify_post', modify_post, methods=['POST'])
