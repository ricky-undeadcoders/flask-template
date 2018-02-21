#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import (render_template, g, current_app, request, abort)
import requests

from application.bp.main.redis_utils import get_reddit_content


def decide_draft():
    request_vars = filter(lambda a: a != '', str(request.url_rule).split('/'))
    if 'draft' in request_vars:
        return True
    return False


def index():
    subreddit_dict = get_reddit_content()
    return render_template('main/home_page.html',
                           subreddit_dict=subreddit_dict,
                           draft=decide_draft())


def about():
    return render_template('main/about_page.html',
                           draft=decide_draft())


def contact():
    return render_template('main/contact_page.html',
                           draft=decide_draft())


def faq():
    return render_template('main/faq.html')
