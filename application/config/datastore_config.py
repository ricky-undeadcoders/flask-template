#!/usr/bin/python3
# -*- coding: utf-8 -*-

USER_FIRST_NAME_MAX_LENGTH = 50
USER_FIRST_NAME_REGEX = '^[a-zA-Z]*$'
USER_LAST_NAME_MAX_LENGTH = 50
USER_LAST_NAME_REGEX = '^[a-zA-Z]*$'
USER_PASSWORD_MAX_LENGTH = 20
USER_PASSWORD_MIN_LENGTH = 8
USER_PASSWORD_REGEX = '^[a-zA-Z0-9_.!@#$%^&*(),?/\;:]*$'
USER_USERNAME_MAX_LENGTH = 20
USER_USERNAME_REGEX = '^[a-zA-Z0-9_.]*$'
USER_EMAIL_MAX_LENGTH = 50
USER_EMAIL_REGEX = '^[a-zA-Z0-9_.@!#$%^&*()_+=,<>/?[]{}"'']*$'
USER_BIO_MAX_LENGTH = 2048

ROLE_NAME_MAX_LENGTH = 25
ROLE_NAME_REGEX = '^[a-zA-Z]*$'
ROLE_DESCRIPTION_MAX_LENGTH = 100
ROLE_DESCRIPTION_REGEX = '^[a-zA-Z ]*$'

CONTENT_TEXT_MAX_LENGTH = 10000

POST_TITLE_MAX_LENGTH = 10000
POST_BODY_MAX_LENGTH = 10000

PAGINATION_CONFIG = {
    'users': {
        'model': 'User',
        'is_admin': False,
        'per_page': 20,
        'search_fields': ['username', 'first_name', 'last_name', 'email']
    },
    'admin_users': {
        'model': 'User',
        'is_admin': True,
        'per_page': 20,
        'search_fields': ['username', 'first_name', 'last_name', 'email']
    },
    'roles': {
        'model': 'Role',
        'is_admin': False,
        'per_page': 20,
        'search_fields': ['name', 'description']
    },
    'admin_roles': {
        'model': 'Role',
        'is_admin': True,
        'per_page': 20,
        'search_fields': ['name', 'description']
    },
    'blog': {
        'model': 'Post',
        'per_page': 10,
        'search_fields': ['title', 'body']  # 'username' doesn't work yet b/c of User relationship
    },
    'faq': {
        'model': 'FAQ',
        'per_page': 10,
        'search_fields': ['question', 'answer']
    }
}

FAQ_QUESTION_MAX_LENGTH = 1024
FAQ_ANSWER_MAX_LENGTH = 2048
