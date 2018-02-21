#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask_security import Security
from flask_mail import Mail
from flask_redis import FlaskRedis
from mockredis import MockRedis


class BaseSecurity(Security):
    """
    Using this to alter the blueprint login redirect config option in LoginManager
    Flask-Security bypasses this config point entirely
    """

    def __init__(self):
        Security.__init__(self)

    def init_app(self, app, datastore=None, register_blueprint=False,
                 login_form=None, confirm_register_form=None,
                 register_form=None, forgot_password_form=None,
                 reset_password_form=None, change_password_form=None,
                 send_confirmation_form=None, passwordless_login_form=None,
                 anonymous_user=None):
        Security.init_app(self, app, datastore, register_blueprint, login_form,
                          confirm_register_form, register_form, forgot_password_form,
                          reset_password_form, change_password_form, send_confirmation_form,
                          passwordless_login_form, anonymous_user)
        app.login_manager.blueprint_login_views = app.config['BLUEPRINT_LOGIN_VIEWS']


class MockRedisWrapper(MockRedis):
    '''A wrapper to add the `from_url` classmethod'''

    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()

    @classmethod
    def set(cls, name, value, **kwargs):
        MockRedis.redis[name] = value

    @classmethod
    def setex(cls, name, time, value):
        MockRedis.redis[name] = value


def create_redis_store(testing=False):
    if testing:
        redis_store = FlaskRedis.from_custom_provider(MockRedisWrapper)
    else:
        redis_store = FlaskRedis()
    return redis_store


security = BaseSecurity()
mail = Mail()
