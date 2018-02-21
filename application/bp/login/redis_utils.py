#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import g
from datetime import timedelta


def set_new_email(user, email):
    time_kws = {'days': 5}
    expiration = timedelta(**time_kws)
    redis_key = 'new_email_{}'.format(user.id)
    g.redis_store.setex(name=redis_key, value=email, time=expiration)


def get_new_email(user):
    redis_key = 'new_email_{}'.format(user.id)
    value = g.redis_store.get(name=redis_key)
    g.redis_store.expire(name=redis_key, time=0)
    return value
