#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bp.admin import blueprint as admin_bp
from bp.login import blueprint as login_bp
from bp.main import blueprint as main_bp
from bp.blog import blueprint as blog_bp

blueprints = [admin_bp, login_bp, main_bp, blog_bp]
