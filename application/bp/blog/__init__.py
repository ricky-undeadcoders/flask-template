#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint

from application.bp.blog.views_html import (blog,
                                            blog_post,
                                            blog_archives,
                                            authors,
                                            author_details)

blueprint = Blueprint(name='blog',
                      import_name=__name__,
                      url_prefix='/blog')
blueprint.__version__ = '1.0.0'

##############################################
# HTML RULES
##############################################
blueprint.add_url_rule('/', 'blog', blog, methods=['GET'])
blueprint.add_url_rule('/<int:post_id>/', 'blog_post', blog_post, methods=['GET'])
blueprint.add_url_rule('/archives/', 'blog_archives', blog_archives, methods=['GET'])
blueprint.add_url_rule('/authors/', 'authors', authors, methods=['GET'])
blueprint.add_url_rule('/authors/<int:user_id>/', 'author_details', author_details, methods=['GET'])
