from flask.ext.sqlalchemy import SQLAlchemy

from app import views

# adding all
from flask import Flask, session, redirect, url_for, escape, request, render_template,flash
from flask_wtf import Form
from flask import Blueprint
import json, subprocess, os
import datetime, logging
from logging import Formatter, FileHandler
import os
from config import * #not a good way

#registering blueprints

from app.views import messageHandle
from app.models.custom_classes import MomentJs
from app.models.user import User
from app.models.messages import Messages

from app.db import db
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask


def url_for_other_page(page):
    url_args = dict(request.args)
    url_args.update(request.view_args)
    url_args['page'] = page
    return url_for(request.endpoint, **url_args)



def build_url(*args, **kwargs):
    return Href(url_root())(*args, **kwargs)


def is_safe_url(target):
    ref_url = urlsplit(request.host_url)
    test_url = urlsplit(urljoin(request.host_url, target))

    is_http = test_url.scheme in ('http', 'https')
    same_host = ref_url.netloc == test_url.netloc

    return is_http and same_host


def get_redirect_next(default=None):
    next = request.values.get('next')
    if next and is_safe_url(next):
        return next
    return default


def get_redirect_back(default=None):
    if is_safe_url(request.referrer):
        return request.referrer
    return default


def app_init():
    capp = Flask(__name__, static_folder='../static')
    capp.config.from_object('config')
    db.init_app(capp)

    # Removed this as it was conflicting with Flask- migrate
    #with capp.app_context():
    #    db.create_all()
    capp.debug = True
    capp.register_blueprint(messageHandle)

    capp.add_url_rule(
        '/models/<int:make_id>/', view_func=views.ModelsAPI.as_view('models_api'),
        methods=['GET'])

    capp.jinja_env.globals.update({
        'url_for_other_page': url_for_other_page,
        'moment': MomentJs,
        'get_redirect_back': get_redirect_back,
        'get_redirect_next': get_redirect_next,
        'is_safe_url': is_safe_url,
        'build_url': build_url

    })

    return capp, db
