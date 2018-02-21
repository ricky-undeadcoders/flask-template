#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Blueprint

from application.bp.main.views_html import (index,
                                            about,
                                            contact,
                                            faq)

blueprint = Blueprint(name='main',
                      import_name=__name__)
blueprint.__version__ = '1.0.0'

##############################################
# HTML RULES
##############################################
blueprint.add_url_rule('/', 'index', index, methods=['GET'])
blueprint.add_url_rule('/about/', 'about', about, methods=['GET'])
blueprint.add_url_rule('/contact/', 'contact', contact, methods=['GET'])
blueprint.add_url_rule('/faq/', 'faq', faq, methods=['GET'])

# DRAFT RULES
blueprint.add_url_rule('/draft/', 'draft', index, methods=['GET'])
blueprint.add_url_rule('/draft/about/', 'draft_about', about, methods=['GET'])
blueprint.add_url_rule('/draft/contact/', 'draft_contact', contact, methods=['GET'])

