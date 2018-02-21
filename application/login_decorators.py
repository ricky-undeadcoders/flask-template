#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import wraps
from flask import current_app, redirect, url_for, request, session
from flask_security import current_user, logout_user


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        if not current_user.is_authenticated:
            session['next'] = request.url_rule.endpoint
            return redirect(url_for(current_app.login_manager.blueprint_login_views.get('login', 'login.login')))
        return func(*args, **kwargs)

    return decorated_view


def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        if not current_user.is_authenticated:
            session['next'] = request.url_rule.endpoint
            return redirect(url_for(current_app.login_manager.blueprint_login_views.get('admin', 'admin.login')))
        if not current_user.has_role('admin'):
            return current_app.login_manager.unauthorized()

        return func(*args, **kwargs)

    return decorated_view
