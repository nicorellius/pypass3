from flask import (request, session, redirect,
                   url_for, render_template, flash,
                   abort)

from flask_login import login_user, logout_user, current_user

from . import utils
from . import config

from .oauth import OAuthSignIn

from .generate import generate_secret
from .application import app, mongo
from .models import User


# Start views for main application
@app.route('/', methods=['GET'])
def home():

    return render_template('generate.html')


# Start views for main application
@app.route('/settings', methods=['GET', 'POST'])
def settings():

    return render_template('settings.html')


# Start views for main application
@app.route('/manage', methods=['GET', 'POST'])
def manage():

    return render_template('manage.html')


# Start views for main application
@app.route('/profile', methods=['GET', 'POST'])
def profile():

    return render_template('profile.html')


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
            flash('You were logged in successfully', 'notifications')

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

            utils.log_output_params(output_type, dice, rolls, length, num)

            return redirect(url_for('home'))

        except Exception as e:
            print(("Exception: {0}".format(e)))


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

        dbu = mongo.db.users.find_one({'social_id': social_id})
        print('just queried mongo...')

        try:
            user = User(username=dbu['username'],
                        social_id=dbu['social_id'],
                        email=dbu['email'])
            print('just created user...')
            print('user: ' + user.username)

        except TypeError as te:
            user = None
            print('TypeError: {0}'.format(te))

        config.logger.info('[{0}] Me in oauth_callback: {1}'.format(
            utils.get_timestamp(), dbu))

        if user is None and dbu is None:
            print('no user...   ')

            try:
                print('trying to create new user...')
                user = User(username=username, social_id=social_id, email=email)
                # TODO  find way to check for duplicate entry, eg, like
                # TODO  Integrity error for SQLite. Enforce uniqueness for this
                # TODO  document, eg, user...
                mongo.db.users.insert({
                    'username': user.username,
                    'social_id': user.social_id,
                    'email': user.email
                })

                config.logger.info('[{0}] New user created: {1}'.format(
                    utils.get_timestamp(), user))

            # TODO: better exception here for duplicate? Or remove?
            except ValueError:
                login_user(user, True)
                session['logged_in'] = True
                flash("Only one '{0}' can access this system.\n"
                      "Logged in as 'guest' instead.".format(username),
                      'notifications')

                return redirect(url_for('home'))

        login_user(user, True)
        session['logged_in'] = True
        flash('You were logged in successfully', 'notifications')

        return redirect(url_for('home'))

    except TypeError as te:
        print("Seems something is wrong with provider's response")
        print('TypeError: {0}'.format(te))
        flash('Something went wrong... Authentication error', 'errors')

    return render_template('login.html')

