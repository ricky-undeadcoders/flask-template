#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import (g, request)
from functools import wraps


def generate_pagination(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.get('item_pagination'):
            q = request.args.get('q', '')
            sort = request.args.get('sort', 'create_date')
            direction = request.args.get('direction', 'desc')
            page = int(request.args.get('page') or 1)
            endpoint = request.endpoint.split('.')[1]
            query = g.datastore.paginate_items(page, q, endpoint, sort, direction)
            g.item_pagination = query
        return f(*args, **kwargs)
    return decorated_function
