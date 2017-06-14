"""
PyPass3

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Character 
Password Generator

Mozilla Public License Version 2
https://www.mozilla.org/en-US/MPL/2.0/

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

"""

from sqlalchemy.exc import IntegrityError

from flask import (Flask, request, session, redirect,
                   url_for, abort, render_template, flash)

from flask_login import LoginManager, login_user, logout_user, current_user

from flask_pymongo import PyMongo
from pymongo import errors as pymongo_errors

from . import utils
from . import config

from .models import User
from .oauth import OAuthSignIn
from .csrf import csrf
from .generate import generate_secret

# Main list of items to do...
# TODO: Encrypt everything going into database
# TODO: Build out logging application of module
# TODO: Implement forms with proper validation for login and genberate

# Configure Flask application
app = Flask(__name__)

app.config.update(config.appconf)
app.config.from_object(__name__)
# app.config.from_envvar('PYPASS_SETTINGS', silent=True)

# Protect with CSRF
csrf(app)

# MongoDB
mongo = PyMongo(app)

# db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'

if app.debug is True:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)


# Start views for main application
@app.route('/', methods=['GET'])
def home():

    # secrets = mongo.db.secret_collection.find_one()
    return render_template('generate.html')  # , secrets=secrets)


@app.route('/generate', methods=['POST'])
# @login_required
def generate():

    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':

        # TODO: add validation for form input (javascript, as well?)
        output_type = request.form.get('type', 'words')
        dice = request.form.get('dice', 5)
        rolls = request.form.get('rolls', 5)
        length = request.form.get('length', 20)
        num = 1

        if not length:
            length = 20

        else:
            length = int(length)

        if output_type is 'mixed' or output_type is 'numbers':
            dice, rolls = 5, 5

        elif output_type == 'uuid':

            if length > 32:
                flash("UUID can be a maximum of 32 characters", 'notifications')

            elif length == 32:
                secret = utils.gen_uid()
                flash(secret, 'secrets')

            else:
                secret = utils.gen_uid(length, True)
                flash(secret, 'secrets')

            return redirect(url_for('home'))

        try:
            secret = generate_secret(number_rolls=int(rolls),
                                     number_dice=int(dice),
                                     how_many=num,
                                     output_type=str(output_type),
                                     secret_length=length)

            flash(secret, 'secrets')

            _log_output_params(output_type, dice, rolls, length, num)

            return redirect(url_for('home'))

        except ValueError as ve:
            print("ValueError: {0}".format(ve))


@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        config_user = app.config['USERNAME']
        config_pass = app.config['PASSWORD']

        if username != config_user or password != config_pass:
            error = 'Invalid username or password'
            flash(error, 'errors')

        session['logged_in'] = True
        flash('You were logged in', 'notifications')

        return redirect(url_for('home'))

    # TODO: with flashing, this dict is not needed...
    data = {'error': error}

    return render_template('login.html', **data)


@app.route('/logout', methods=['GET'])
def logout():

    session.pop('logged_in', None)
    logout_user()
    flash('You were logged out', 'notifications')

    return redirect(url_for('login'))


def _log_output_params(output_type, dice, rolls, length, num):

    return config.logger.info(
        '[{0}] Parameters:\n'
        '        output type: {1} {2}\n'
        '     number of dice: {3}     {4}\n'
        '    number of rolls: {5}     {6}\n'
        '      secret length: {7}    {8}\n'
        '  number of secrets: {9}     {10}'.format(
            utils.get_timestamp(),
            output_type, type(output_type),
            dice, type(dice),
            rolls, type(rolls),
            length, type(length),
            num, type(num))
    )


@login_manager.user_loader
def load_user(username):

    user = mongo.db.users_collection.find_one({
        'username': username})

    if not user:
        return None

    return User(user['username'], user['social_id'], user['email'])


@app.route('/authorize/<provider>')
def oauth_authorize(provider):

    config.logger.info('[{0}] Before get_provider: {1}'.format(
        utils.get_timestamp(), str(provider)))

    if not current_user.is_anonymous:
        return redirect(url_for('home'))

    oauth = OAuthSignIn.get_provider(provider)

    config.logger.info('[{0}] After get_provider: {1}'.format(
        utils.get_timestamp(), str(provider)))

    config.logger.info('[{0}] OAuth authorize: {1}'.format(
        utils.get_timestamp(), oauth.authorize()))

    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):

    user = ''
    username = ''
    social_id = ''
    email = ''

    if not current_user.is_anonymous:
        return redirect(url_for('home'))

    oauth = OAuthSignIn.get_provider(provider)

    try:
        social_id, username, email = oauth.callback()
        config.logger.info('[{0}] OAuth object: {1}'.format(
            utils.get_timestamp(), oauth))

        if social_id is None:
            flash('Authentication failed.')
            return redirect(url_for('home'))

    except TypeError as te:
        print("TypeError in assigning callback: {0}".format(te))
        flash("Something went wrong with your authentication", 'errors')

    try:
        user_db = mongo.db.users_collection.find_one({
            'username': username})

        # print(user_db['username'])  # prints username from db user
        # user = User(str(user_db['username']))  # create user object

        user = User(user_db['username'],
                    user_db['social_id'],
                    user_db['email'])

        config.logger.info('[{0}] User from database: {1} {2}'.format(
            utils.get_timestamp(), user, type(user)))

    except KeyError as ke:
        print("KeyError: {0} not found in response".format(ke))

    except TypeError as te:
        print("TypeError in finding/creating user: {0}".format(te))

    if user is 'guest':
        try:
            collection = mongo.db.users_collection
            user = {
                'username': username,
                'social_id': social_id,
                'email': email,
            }
            collection.insert_one(user)

        except IntegrityError:

            login_user(user, True)
            session['logged_in'] = True
            flash("Only one '{0}' can access this system.\n"
                  "Logged in as 'guest' instead.".format(username),
                  'notifications')

            return redirect(url_for('home'))

    try:
        login_user(user, True)
        session['logged_in'] = True
        flash("You were logged in", 'notifications')
        return redirect(url_for('home'))

    except AttributeError as ae:
        print("AttributeError: {0}".format(ae))
        flash("Oops... Something went wrong. Try again.",
              'errors')

    return render_template('login.html')

