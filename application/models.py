#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask_security import UserMixin, RoleMixin, AnonymousUser
from sqlalchemy import (Table, Column, Integer, ForeignKey, String, Boolean, ColumnDefault, DateTime,
                        CheckConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (ChoiceType)
from datetime import datetime

from application.config import datastore_config as ds_config

Base = declarative_base()
metadata = Base.metadata


class CustomAnonymousUser(AnonymousUser):
    def __init__(self):
        AnonymousUser.__init__(self)

    @property
    def is_admin_user(self):
        return False


################################################
# RELATIONSHIPS
################################################

user_roles = Table('user_roles', metadata,
                   Column('role_id', Integer, ForeignKey('role.id')),
                   Column('user_id', Integer, ForeignKey('user.id')))


class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    password = Column(String(length=255), nullable=False)
    username = Column(String(length=ds_config.USER_USERNAME_MAX_LENGTH), unique=True)
    first_name = Column(String(length=ds_config.USER_FIRST_NAME_MAX_LENGTH))
    last_name = Column(String(length=ds_config.USER_LAST_NAME_MAX_LENGTH))
    email = Column(String(length=ds_config.USER_EMAIL_MAX_LENGTH), unique=True, nullable=False)
    is_admin = Column(Boolean(), ColumnDefault(False))

    roles = relationship('Role', secondary=user_roles)
    bio = relationship('Bio', back_populates='user', uselist=False)
    posts = relationship('Post', back_populates='user')

    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(length=25))
    current_login_ip = Column(String(length=25))
    login_count = Column(Integer(), ColumnDefault(0))
    confirmed_at = Column(DateTime())
    active = Column(Boolean(), ColumnDefault(True))
    create_date = Column(DateTime(), ColumnDefault(datetime.utcnow()))
    updated_date = Column(DateTime(), ColumnDefault(datetime.utcnow(), for_update=True))

    @property
    def is_admin_user(self):
        for role in self.roles:
            if role.name == 'admin':
                return True
        return False


class Role(Base, RoleMixin):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=ds_config.ROLE_NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(String(length=ds_config.ROLE_DESCRIPTION_MAX_LENGTH))
    is_admin = Column(Boolean(), ColumnDefault(False))

    users = relationship('User', secondary=user_roles)

    active = Column(Boolean(), ColumnDefault(True))
    create_date = Column(DateTime(), ColumnDefault(datetime.utcnow()))
    updated_date = Column(DateTime(), ColumnDefault(datetime.utcnow(), for_update=True))


class Bio(Base):
    __tablename__ = 'bio'

    id = Column(Integer, primary_key=True)
    text = Column(String(length=ds_config.USER_BIO_MAX_LENGTH))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='bio')


class Content(Base):
    __tablename__ = 'content'

    site_fields = [(u'home_page_title', u'Home Page Title'),
                   (u'welcome_wiget_body', u'About Widget Text'),
                   (u'about_page_body', u'About Page Body Text'),
                   (u'contact_page_body', u'Contact Page Body Text')]

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_name = Column(ChoiceType(site_fields))
    text = Column(String(length=ds_config.CONTENT_TEXT_MAX_LENGTH))

    create_date = Column(DateTime(), ColumnDefault(datetime.utcnow()))
    updated_date = Column(DateTime(), ColumnDefault(datetime.utcnow(), for_update=True))


class ContentDraft(Base):
    __tablename__ = 'content_draft'

    site_fields = [(u'home_page_title', u'Home Page Title'),
                   (u'welcome_wiget_body', u'About Widget Text'),
                   (u'about_page_body', u'About Page Body Text'),
                   (u'contact_page_body', u'Contact Page Body Text')]

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_name = Column(ChoiceType(site_fields))
    text = Column(String(length=ds_config.CONTENT_TEXT_MAX_LENGTH))

    create_date = Column(DateTime(), ColumnDefault(datetime.utcnow()))
    updated_date = Column(DateTime(), ColumnDefault(datetime.utcnow(), for_update=True))


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('user.id'))
    user = relationship('User', back_populates='posts')
    title = Column(String(length=ds_config.POST_TITLE_MAX_LENGTH))
    body = Column(String(length=ds_config.POST_BODY_MAX_LENGTH))

    active = Column(Boolean(), ColumnDefault(False))
    create_date = Column(DateTime(), ColumnDefault(datetime.utcnow()))
    updated_date = Column(DateTime(), ColumnDefault(datetime.utcnow(), for_update=True))


class FAQ(Base):
    __tablename__ = 'faq'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order = Column(Integer, nullable=False)
    question = Column(String(length=ds_config.FAQ_QUESTION_MAX_LENGTH), nullable=False)
    answer = Column(String(length=ds_config.FAQ_ANSWER_MAX_LENGTH), nullable=False)

    active = Column(Boolean(), ColumnDefault(False))
    create_date = Column(DateTime(), ColumnDefault(datetime.utcnow()))
    updated_date = Column(DateTime(), ColumnDefault(datetime.utcnow(), for_update=True))


class InvitationEmail(Base):
    __tablename__ = 'invitation_email'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=ds_config.USER_EMAIL_MAX_LENGTH), unique=True)

    create_date = Column(DateTime(), ColumnDefault(datetime.utcnow()))
    updated_date = Column(DateTime(), ColumnDefault(datetime.utcnow(), for_update=True))
