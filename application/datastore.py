# !/usr/bin/python3
# -*- coding: utf-8 -*-


from flask import current_app
from flask_security.utils import get_identity_attributes, string_types
from flask_sqlalchemy import Pagination
from sqlalchemy import func, text, or_, all_

from application import models
from models import *


class BaseDataStore(object):
    def __init__(self, db):
        self.db = db

    #####################################################################
    # BASE FUNCTIONS
    #####################################################################

    def commit(self):
        self.db.session.flush()
        self.db.session.commit()

    def put(self, model):
        self.db.session.add(model)
        self.commit()

    def delete(self, model):
        self.db.session.delete(model)
        self.commit()

    def search(self, q, model):
        if not q:
            return ''

        search_query = '%{0}%'.format(q)
        # search_chain = []

        # for this_field in search_fields:
        #     this_search = model.this_field.ilike(search_query)
        #     search_chain.append(this_search)
        search_chain = [model.email.ilike(search_query),
                        model.username.ilike(search_query),
                        model.first_name.ilike(search_query),
                        model.last_name.ilike(search_query)]

        return or_(*search_chain)

    def _is_numeric(self, value):
        try:
            int(value)
        except (TypeError, ValueError):
            return False
        return True

    def toggle_active(self, model):
        """Toggles a user's active status. Always returns True."""
        try:
            model.active = not model.active
            return True
        except:
            return False

    #####################################################################
    # USER AND ADMIN USER FUNCTIONS
    #####################################################################

    def paginate_items(self, page, q, endpoint, sort, direction):
        pagination_config = ds_config.PAGINATION_CONFIG[endpoint]

        model = eval(pagination_config['model'])
        per_page = pagination_config['per_page']

        order_values = '{0} {1}'.format(sort, direction)

        query = self.db.session.query(model)

        if 'is_admin' in pagination_config.iterkeys():
            is_admin = pagination_config['is_admin']
            query = query.filter_by(is_admin=is_admin)

        search_query = '%{0}%'.format(q)
        search_chain = []

        if endpoint in ['users', 'admin_users']:
            search_chain = [model.email.ilike(search_query),
                            model.username.ilike(search_query),
                            model.first_name.ilike(search_query),
                            model.last_name.ilike(search_query)]
        elif endpoint in ['roles', 'admin_roles']:
            search_chain = [model.name.ilike(search_query),
                            model.description.ilike(search_query)]
        elif endpoint == 'blog':
            search_chain = [model.title.ilike(search_query),
                            model.body.ilike(search_query)]

        if len(search_chain) > 0:
            query = query.filter(or_(*search_chain))
        query = query.order_by(text(order_values))

        return query.paginate(page, per_page, False)

    def get_user(self, identifier):
        if self._is_numeric(identifier):
            return self.db.session.query(User).get(identifier)
        for attr in get_identity_attributes():
            query = func.lower(getattr(User, attr)) \
                    == func.lower(identifier)
            rv = self.db.session.query(User).filter(query).first()
            if rv is not None:
                return rv

    def find_user(self, **kwargs):
        user = self.db.session.query(User).filter_by(**kwargs).first()
        return user

    def find_admin_user(self, **kwargs):
        return self.find_user(is_admin=True, **kwargs)

    def deactivate_model(self, model):
        """Deactivates a specified user. Returns `True` if a change was made.

        :param user: The user to deactivate
        """
        try:
            if model.active:
                model.active = False
                return True
            return False
        except:
            return False

    def activate_model(self, model):
        """Activates a specified user. Returns `True` if a change was made.

        :param user: The user to activate
        """
        try:
            if not model.active:
                model.active = True
                return True
            return False
        except:
            return False

    def create_user(self, **kwargs):
        """Creates and returns a new user from the given parameters."""
        user = User(**kwargs)
        self.put(user)
        return user

    def create_admin_user(self, **kwargs):
        """Creates and returns a new user from the given parameters."""
        bio = Bio(text=kwargs.pop('bio'))
        user = User(**kwargs)
        user.is_admin = True
        user.bio = bio
        self.put(user)
        return user

    def find_all_users(self, role=None):
        if role:
            role = self._prepare_role_arg(role)
            users = self.db.session.query(User).filter_by(is_admin=False).all()
            users_with_role = []
            for user in users:
                if role in user.roles:
                    users_with_role.append(user)
            return users_with_role
        return self.db.session.query(User).filter_by(is_admin=False).all()

    def find_all_admin_users(self, role=None):
        if role:
            role = self._prepare_role_arg(role)
            users = self.db.session.query(User).filter_by(is_admin=True).all()
            users_with_role = []
            for user in users:
                if role in user.roles:
                    users_with_role.append(user)
            return users_with_role
        return self.db.session.query(User).filter_by(is_admin=True).all()

    def modify_user(self, user, **kwargs):
        if kwargs.get('username'):
            user.username = kwargs['username']
        if kwargs.get('first_name'):
            user.first_name = kwargs['first_name']
        if kwargs.get('last_name'):
            user.last_name = kwargs['last_name']
        if kwargs.get('first_name'):
            user.first_name = kwargs['first_name']
        if kwargs.get('email'):
            user.email = kwargs['email']
        if kwargs.get('bio'):
            user.bio = Bio(**{'text': kwargs['bio']})
        if kwargs.get('roles'):
            user.roles = kwargs['roles']
        self.put(user)
        return user

    def modify_admin_user(self, user, **kwargs):
        if kwargs.get('bio'):
            user.bio = Bio(**{'text': kwargs['bio']})
        self.modify_user(user, **kwargs)
        return user

    def find_invitation_email(self, **kwargs):
        return self.db.session.query(InvitationEmail).filter_by(**kwargs).first()

    #####################################################################
    # ROLE AND ADMIN ROLE FUNCTIONS
    #####################################################################

    def _prepare_role_modify_args(self, user, role):
        if isinstance(user, string_types):
            user = self.find_user(email=user)
        if isinstance(role, string_types):
            role = self.find_role(role)
        return user, role

    def _prepare_role_arg(self, role):
        if isinstance(role, string_types):
            role = self.find_role(role)
        return role

    def create_role(self, **kwargs):
        """Creates and returns a new role from the given parameters."""
        role = Role(**kwargs)
        self.put(role)
        return role

    def create_admin_role(self, **kwargs):
        """Creates and returns a new role from the given parameters."""

        role = Role(**kwargs)
        role.is_admin = True
        self.put(role)
        return role

    def find_role(self, **kwargs):
        return self.db.session.query(Role).filter_by(is_admin=False, **kwargs).first()

    def find_admin_role(self, **kwargs):
        return self.db.session.query(Role).filter_by(is_admin=True, **kwargs).first()

    def find_all_roles(self):
        # return self.db.session.query(Role).all()
        return self.db.session.query(Role).filter_by(is_admin=False).all()

    def find_all_admin_roles(self):
        return self.db.session.query(Role).filter_by(is_admin=True).all()

    def modify_role(self, role, **kwargs):
        if kwargs.get('name'):
            role.name = kwargs['name']
        if kwargs.get('description'):
            role.description = kwargs['description']
        self.put(role)
        return role

    def add_role_to_user(self, user, role):
        """Adds a role to a user.
        :param user: The user to manipulate
        :param role: The role to add to the user
        """
        user, role = self._prepare_role_modify_args(user, role)
        if role not in user.roles:
            user.roles.append(role)
            self.put(user)
            return user
        return False

    def remove_role_from_user(self, user, role):
        """Removes a role from a user.

        :param user: The user to manipulate
        :param role: The role to remove from the user
        """
        rv = False
        user, role = self._prepare_role_modify_args(user, role)
        if role in user.roles:
            rv = True
            user.roles.remove(role)
            self.put(user)
        return rv

    #####################################################################
    # CONTENT FUNCTIONS
    #####################################################################

    def create_faq(self, **kwargs):
        """Creates and returns a new role from the given parameters."""
        faq = FAQ(**kwargs)
        self.put(faq)
        return faq

    def modify_faq(self, faq, **kwargs):
        if kwargs.get('order'):
            faq.order = kwargs['order']
        if kwargs.get('question'):
            faq.question = kwargs['question']
        if kwargs.get('answer'):
            faq.answer = kwargs['answer']
        self.put(faq)
        return faq

    def find_faq(self, **kwargs):
        return self.db.session.query(FAQ).filter_by(**kwargs).first()

    def find_all_faq(self, order_by=None):
        if order_by:
            try:
                return self.db.session.query(FAQ).order_by(order_by).all()
            except:
                pass
        return self.db.session.query(FAQ).order_by('order').all()

    #####################################################################
    # CONTENT FUNCTIONS
    #####################################################################

    def find_content(self, field_name, draft=False):
        if draft:
            return self.db.session.query(ContentDraft).filter_by(field_name=field_name).first()
        return self.db.session.query(Content).filter_by(field_name=field_name).first()

    def modify_content_draft(self, content, **kwargs):
        if kwargs.get('description'):
            content.description = kwargs['description']
        if kwargs.get('text'):
            content.text = kwargs['text']
        self.put(content)
        return content

    def publish_content(self, content, content_draft):
        content.text = content_draft.text
        self.put(content)
        return content

    #############################################################
    # POST FUNCTIONS
    #############################################################

    def create_post(self, **kwargs):
        """Creates and returns a new blog post from the given parameters."""
        post = Post(**kwargs)
        self.put(post)
        return post

    def find_post(self, **kwargs):
        return self.db.session.query(Post).filter_by(**kwargs).first()

    def find_all_posts(self, order_by=None, **kwargs):
        if order_by:
            try:
                return self.db.session.query(Post).filter_by(**kwargs).order_by(order_by).all()
            except:
                pass
        return self.db.session.query(Post).filter_by(**kwargs).order_by('id').all()

    def modify_post(self, post, **kwargs):
        if kwargs.get('title'):
            post.title = kwargs['title']
        if kwargs.get('body'):
            post.body = kwargs['body']
        if kwargs.get('toggle_active'):
            self.toggle_active(post)
        self.put(post)
        return post
