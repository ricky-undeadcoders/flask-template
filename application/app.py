#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, g, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss

from logging.config import dictConfig
import logging

from models import (CustomAnonymousUser)

from blueprints import blueprints
from config import base_config, production_config, datastore_config, verbiage_config
from datastore import BaseDataStore
from extensions import security, mail, create_redis_store
from application import __version__
from template_filters import template_filters


#################################################
# BUILD OUR FLASK APPLICATION
#################################################

def create_app(configs=None):
    app = Flask(import_name=__name__)
    app.config.from_object(base_config)
    app.config.from_object(datastore_config)
    app.config.from_object(verbiage_config)

    if configs:
        for config in configs:
            app.config.from_object(config)
    else:
        # Remove default handlers for one of our own
        [app.logger.removeHandler(handler) for handler in app.logger.handlers]
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
        app.logger.addHandler(handler)
        #     # TODO: Switch production to pull from environment vars
        #     # app.config.from_object(os.environ['APP_SETTINGS'])
        app.logger.exception('We are loading production config!')
        app.config.from_object(production_config)

    app.logger.info('Loaded app with configs, launching datastore')
    db = SQLAlchemy(app)
    user_datastore = BaseDataStore(db=db)

    app.logger.info('Launching extensions')
    security.init_app(app=app,
                      datastore=user_datastore,
                      anonymous_user=CustomAnonymousUser,
                      register_blueprint=False)
    mail.init_app(app)
    redis_store = create_redis_store(app.testing)
    redis_store.init_app(app)

    app.logger.info('Adding blueprints')
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    app.logger.info('Instantiating Scss object')
    Scss(app)

    app.logger.info('Now adding error handling and before_request commands')

    @app.errorhandler(404)
    def page_not_found(e):
        return '404 Not Found :-(', 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return 'Server Error', 405

    @app.errorhandler(500)
    def server_error(e):
        return '500 error', 500

    @app.before_request
    def before_request():
        try:
            # set up easier reference to our datastore, also error check that it exists
            g.datastore = app.extensions['security'].datastore
            g.redis_store = app.extensions['redis']
        except Exception, e:
            app.logger.critical('Security extension is not registered or has no datastore: {}'.format(e))
            abort(500)

    @app.after_request
    def add_header(response):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response

    app.logger.info('Aaaaaaaannnnndddddd basic views.....')

    @app.route('/version/', methods=['GET'])
    def version():
        return __version__

    @app.route('/site-map/', methods=['GET'])
    def site_map():
        view_functions = []
        for url_rule, url_function in app.view_functions.iteritems():
            try:
                bp, view = url_rule.split('.')
                if bp in app.config['SITE_MAP_BLUEPRINTS'] and 'draft' not in view:
                    view_functions.append((url_rule, url_for(url_rule)))
            except:
                pass
        view_functions.sort()
        return render_template('main/site_map.html',
                               view_functions=view_functions)

    app.logger.debug('And template filters......')
    for template_filter in template_filters:
        app.add_template_filter(template_filter)

    @app.route('/tester/')
    def tester():
        return render_template('blog/admin/post.html')

    return app