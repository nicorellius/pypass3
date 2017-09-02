"""
PyPass3

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Character 
Password Generator

Mozilla Public License Version 2
https://www.mozilla.org/en-US/MPL/2.0/

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

"""

from flask import Flask

from flask_login import LoginManager, UserMixin
# from flask_pymongo import PyMongo

# TODO: Consider setting up app like this:
# TODO   http://flask.pocoo.org/docs/0.12/patterns/packages/
# from pypass import app

from . import utils
from . import config

from .mongo import global_init
from .csrf import csrf
from .models.user import User


# TODO: Encrypt everything going into database
# TODO: Build out logging application of module
# TODO: Implement `mongoengine` via `flask-mongoengine`
# TODO: Substitute `rdoclient` for forked `rdoclient-py3`

# Configure Flask application
app = Flask(__name__,
            template_folder=config.TEMPLATE_PATH,
            static_folder=config.STATIC_PATH)
app.config.update(config.appconf)
app.config.from_object(__name__)
app.config.from_envvar('PYPASS_SETTINGS', silent=True)

# Protect with CSRF
csrf(app)

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
    config.logger.info('[{0}] Views imported: {1}'.format(
        utils.get_timestamp(), str(views.__file__)))
else:
    raise ImportError


GUEST_USER = {
    'username': 'guest',
    'social_id': 'guest',
    'email': 'guest'
}


def config_mongo():
    global_init()


@login_manager.user_loader
def load_user(username):

    user = User.objects().find_one({
        'username': username})

    if not user:
        return None

    return User(user['username'], user['social_id'], user['email'])
