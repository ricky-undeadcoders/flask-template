#!/usr/bin/python3
#  -*- coding: utf-8 -*-
from datetime import datetime as DT
from datetime import date as DATE
from pytz import (timezone, utc)
from types import (UnicodeType, StringType, ListType)
from flask import (flash, current_app, request, make_response, render_template)
import re
from json import dumps

datetime_format = '%Y-%m-%d %H:%M'
date_format = '%Y-%m-%d'
time_format = '%H:%M'
pretty_date_format = '%b %d, %Y'
pretty_time_format = '%I:%M %p'
central = timezone('US/Central')


def jsonify(text):
    return dumps(text)


def convert_utc_datetime_to_central(datetime):
    if isinstance(datetime, DT):
        local_dt = utc.localize(datetime).astimezone(central)
        return local_dt
    if isinstance(datetime, UnicodeType):
        local_dt = utc.localize(DT.strptime(datetime, datetime_format)).astimezone(central)
        return local_dt.strftime(datetime_format)


def convert_central_datetime_to_utc(datetime):
    if isinstance(datetime, DT):
        local_dt = central.localize(datetime)
        return utc.normalize(local_dt)
    if isinstance(datetime, UnicodeType):
        local_dt = central.localize(DT.strptime(datetime, datetime_format))
        utc_datetime = utc.normalize(local_dt)
        return utc_datetime.strftime(datetime_format)


def join_date_and_time_to_utc(date, time, output_type='string'):
    """
    accepts a UTC date and time object or Unicode strings
    returns a datetime that is of the same type as input and in Central timezone
    """
    if all([isinstance(date, UnicodeType), isinstance(time, UnicodeType)]) or all(
            [isinstance(date, StringType), isinstance(time, StringType)]):
        try:
            datetime_string = '{} {}'.format(date.strip(), time.strip())
            datetime_obj = DT.strptime(datetime_string, datetime_format)
            utc_datetime_obj = convert_central_datetime_to_utc(datetime_obj)
            if output_type.lower() == 'datetime':
                return utc_datetime_obj
            return utc_datetime_obj.strftime(datetime_format)
        except Exception, e:
            return DT.strptime('1900-01-01 00:00', datetime_format)
    if all([isinstance(date, DT), isinstance(time, DT)]):
        try:
            date_string = date.strftime(date_format)
            time_string = date.strftime(time_format)
            datetime_string = '{} {}'.format(date_string.strip(), time_string.strip())
            datetime_obj = DT.strptime(datetime_string, datetime_format)
            utc_datetime_obj = convert_central_datetime_to_utc(datetime_obj)
            if output_type.lower() == 'datetime':
                return utc_datetime_obj
            return utc_datetime_obj.strftime(datetime_format)
        except:
            return DT.strptime('1900-01-01 00:00', datetime_format)
    if all([isinstance(date, DATE), isinstance(time, UnicodeType)]):
        try:
            date_string = date.strftime(date_format)
            datetime_string = '{} {}'.format(date_string.strip(), time.strip())
            datetime_obj = DT.strptime(datetime_string, datetime_format)
            local_datetime_obj = convert_central_datetime_to_utc(datetime_obj)
            if output_type.lower() == 'datetime':
                return local_datetime_obj
            return local_datetime_obj.strftime(datetime_format)
        except Exception, e:
            return DT.strptime('1900-01-01 00:00', datetime_format)


def join_date_and_time_to_central(date, time, output_type='string'):
    """
    accepts a UTC date and time object or Unicode strings
    returns a datetime that is of the same type as input and in Central timezone
    """
    if all([isinstance(date, UnicodeType), isinstance(time, UnicodeType)]):
        try:
            datetime_string = '{} {}'.format(date.strip(), time.strip())
            datetime_obj = DT.strptime(datetime_string, datetime_format)
            local_datetime_obj = convert_utc_datetime_to_central(datetime_obj)
            if output_type.lower() == 'datetime':
                return local_datetime_obj
            return local_datetime_obj.strftime(datetime_format)
        except Exception, e:
            return DT.strptime('1900-01-01 00:00', datetime_format)
    if all([isinstance(date, DT), isinstance(time, DT)]):
        try:
            date_string = date.strftime(date_format)
            time_string = date.strftime(time_format)
            datetime_string = '{} {}'.format(date_string.strip(), time_string.strip())
            datetime_obj = DT.strptime(datetime_string, datetime_format)
            local_datetime_obj = convert_utc_datetime_to_central(datetime_obj)
            if output_type.lower() == 'datetime':
                return local_datetime_obj
            return local_datetime_obj.strftime(datetime_format)
        except:
            return DT.strptime('1900-01-01 00:00', datetime_format)
    if all([isinstance(date, DATE), isinstance(time, UnicodeType)]):
        try:
            date_string = date.strftime(date_format)
            datetime_string = '{} {}'.format(date_string.strip(), time.strip())
            datetime_obj = DT.strptime(datetime_string, datetime_format)
            local_datetime_obj = convert_utc_datetime_to_central(datetime_obj)
            if output_type.lower() == 'datetime':
                return local_datetime_obj
            return local_datetime_obj.strftime(datetime_format)
        except Exception, e:
            return DT.strptime('1900-01-01 00:00', datetime_format)


def split_datetime(datetime, output_type='string'):
    """
    accepts a UTC datetime object or Unicode string
    returns a date and time that are of the same type as input and in Central timezone
    """
    if isinstance(datetime, DT):
        try:
            # do work
            local_datetime = convert_utc_datetime_to_central(datetime)
            date_string = local_datetime.strftime(date_format)
            time_string = local_datetime.strftime(time_format)
            date_obj = DT.strptime(date_string, date_format)
            time_obj = DT.strptime(time_string, time_format)
            if output_type == 'datetime':
                return date_obj, time_obj
            return date_obj.strftime(date_format), time_obj.strftime(time_format)
        except Exception, e:
            print e
            return DT.strptime('1900-01-01', date_format), DT.strptime('00:00', time_format)
    if isinstance(datetime, UnicodeType):
        try:
            # run a test to verify incoming string matches correct format
            DT.strptime(datetime, datetime_format)
            local_datetime = convert_utc_datetime_to_central(datetime)

            # do work
            date_string, time_string = local_datetime.split(' ')
            date_obj = DT.strptime(date_string, date_format)
            time_obj = DT.strptime(time_string, time_format)
            if output_type == 'datetime':
                return date_obj, time_obj
            return date_obj.strftime(date_format), time_obj.strftime(time_format)
        except Exception, e:
            return DT.strptime('1900-01-01', date_format), DT.strptime('00:00', time_format)


def pretty_date(date):
    if isinstance(date, UnicodeType) or isinstance(date, StringType):
        try:
            date_obj = DT.strptime(date, date_format)
            return date_obj.strftime(pretty_date_format)
        except:
            return 'Jan 01, 1900'
    if isinstance(date, DT):
        try:
            date_obj = date
            return date_obj.strftime(pretty_date_format)
        except:
            return DT.strptime('1900-01-01', pretty_date_format)


def pretty_time(time):
    if isinstance(time, UnicodeType) or isinstance(time, StringType):
        try:
            time_obj = DT.strptime(time, time_format)
            return time_obj.strftime(pretty_time_format)
        except:
            return '12:00 AM'
    if isinstance(time, DT):
        try:
            time_obj = time
            return time_obj.strftime(pretty_time_format)
        except:
            return DT.strptime('00:00', pretty_time_format)


def clean_javascript_text(input_string):
    if isinstance(input_string, StringType) or isinstance(input_string, UnicodeType):
        output_string = input_string.replace('"', "'").replace('\r\n', '\n').replace('\n', '<br>')
    else:
        output_string = ''
    return output_string


def format_error_message(error_desc):
    if isinstance(error_desc, ListType):
        return error_desc
    else:
        return [error_desc]


def remove_whitespace(text_data):
    return text_data.replace('\t', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace('\n ','\n').replace('\n\n', '\n').replace('\n', '')


def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '-')

    return s
