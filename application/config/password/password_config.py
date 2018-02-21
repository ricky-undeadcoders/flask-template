#!/usr/bin/python3
# -*- coding: utf-8 -*-

PASSWORD_MIN_LENGTH = 4
PASSWORD_MAX_LENGTH = 20

INCORRECT_PASSWORD_ERROR = 'Your password was incorrect.'
PASSWORD_LENGTH_ERROR = 'This password must be between {} and {} characters.'.format(PASSWORD_MIN_LENGTH,
                                                                                     PASSWORD_MAX_LENGTH)
PASSWORD_WORD_INCLUSION_ERROR = 'Your password includes an invalid word combination. Please see our FAQ for more details.'
PASSWORD_WORD_MATCH_ERROR = 'Your password is invalid. Please see our FAQ for more details.'
PASSWORD_NOT_MATCH_ERROR = 'Your new passwords must match.'
PASSWORD_INVALID_CHARACTER_ERROR = 'Your password contains invalid characters. Please see our FAQ for more details'