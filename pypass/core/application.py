"""
PyPass3

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Character 
Password Generator

Mozilla Public License Version 2
https://www.mozilla.org/en-US/MPL/2.0/

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

"""
import logging

from flask import Flask, flash

from flask_mongoengine import MongoEngine
from flask_mongoengine import DoesNotExist, MultipleObjectsReturned

from flask_login import LoginManager, UserMixin
# from flask_pymongo import PyMongo

# TODO: Consider setting up app like this:
# TODO   http://flask.pocoo.org/docs/0.12/patterns/packages/
# from pypass import app

from apps import logging_setup

from . import utils
from . import config

from .mongo import global_init
from .csrf import csrf
from .models.user import User

# TODO: Implement `mongoengine` via `flask-mongoengine`
# TODO: Substitute `rdoclient` for forked `rdoclient-py3`


logger = logging.getLogger('pypass')


# Configure Flask application
app = Flask(__name__,
            template_folder=config.TEMPLATE_PATH,
            static_folder=config.STATIC_PATH)

app.config.update(config.appconf)
app.config.from_object(__name__)
app.config.from_envvar('PYPASS_SETTINGS', silent=True)

# Protect with CSRF
csrf(app)

# Flask-MongoEngine
db = MongoEngine(app)

# MongoDB with PyMongo
# mongo = PyMongo(app)

# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'home'

if app.debug is True:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)

# Import views after app is created
if app is not None:
    from . import views
    logger.info('Views imported: {0}'.format(str(views.__file__)))
else:
    raise ImportError


GUEST_USER = {
    'username': 'guest',
    'social_id': 'guest',
    'email': 'guest'
}


def config_mongo():
    global_init(user=app.config['MONGODB_USERNAME'],
                password=app.config['MONGODB_PASSWORD'],
                port=app.config['MONGODB_PORT'])


@login_manager.user_loader
def load_user(social_id):

    try:
        return User.objects.get(social_id=social_id)

    except DoesNotExist:
        return None

    except MultipleObjectsReturned:
        flash('Multiple users returned. Only one can be used...')

