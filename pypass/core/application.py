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

from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin,
                         login_user, logout_user, current_user)

from . import utils
from . import config

from .oauth import OAuthSignIn
from .csrf import csrf
from .generate import generate_secret


# TODO: encrypt everything going into database
# TODO: Build out logging application of module

# Configure Flask application
app = Flask(__name__)
app.config.update(config.appconf)
app.config.from_object(__name__)
app.config.from_envvar('PYPASS_SETTINGS', silent=True)

# Protect with CSRF
csrf(app)

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'home'

if app.debug is True:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    def __init__(self, username, social_id, nickname, email=None):
        self.username = username
        self.social_id = social_id
        self.email = email
        self.nickname = nickname

    def __repr__(self):
        return '{0}'.format(self.username)


# Start views for main application
@app.route('/', methods=['GET'])
def home():

    return render_template('generate.html')


@app.route('/generate', methods=['POST'])
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

        except Exception as e:
            print(("Exception: {0}".format(e)))


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

        else:

            session['logged_in'] = True
            flash('You were logged in', 'notifications')

            return redirect(url_for('home'))

    data = {
        'error': error,
    }

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


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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

    if not current_user.is_anonymous:
        return redirect(url_for('home'))

    oauth = OAuthSignIn.get_provider(provider)

    try:
        social_id, username, email = oauth.callback()

        config.logger.info('[{0}] OAuth: {1}'.format(
            utils.get_timestamp(), oauth))

        if social_id is None:
            flash('Authentication failed.')

            return redirect(url_for('home'))

        user = User.query.filter_by(social_id=social_id).first()
        config.logger.info('[{0}] Me in oauth_callback: {1}'.format(
            utils.get_timestamp(), user))

        if not user:

            try:
                user = User(username=username, social_id=social_id,
                            nickname='temp', email=email)
                db.session.add(user)
                db.session.commit()

            except IntegrityError:
                login_user(user, True)
                session['logged_in'] = True
                flash("Only one '{0}' can access this system.\n"
                      "Logged in as 'guest' instead.".format(username),
                      'notifications')
                return redirect(url_for('home'))

        login_user(user, True)
        session['logged_in'] = True
        flash('You were logged in', 'notifications')

        return redirect(url_for('home'))

    except TypeError as ke:
        print("Seems something is wrong with Google's response")
        print('TypeError: {0} not found in response'.format(ke))

    flash('Something went wrong with the authentication', 'errors')

    return render_template('login.html')

db.create_all()

