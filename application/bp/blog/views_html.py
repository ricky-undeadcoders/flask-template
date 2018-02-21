#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import (render_template, g, current_app, abort)


def blog():
    return render_template('blog/blog.html')


def blog_post(post_id):
    post = g.datastore.find_post(id=post_id)
    if not post:
        current_app.logger.error('Post ID was invalid; aborting')
        abort(404)

    return render_template('blog/blog_post.html',
                           post=post)


def blog_archives():
    return render_template('blog/archives.html')


def authors():
    return render_template('blog/authors.html')


def author_details(user_id):
    author = g.datastore.find_user(id=user_id)
    if not author:
        current_app.logger.error('Author or slug were invalid; aborting')
        abort(404)
    return render_template('blog/author_details.html',
                           author=author)
