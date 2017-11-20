import logging

from flask import (request, session, redirect,
                   url_for, render_template, flash,
                   abort)
from flask_login import login_user, logout_user, current_user

from apps.generate import generate_secret
from crypto.encryptor import encrypt_string
from . import config
from . import utils
from .application import app
from .models.secret import Secret
from .models.user import User
from .oauth import OAuthSignIn


logger = logging.getLogger('pypass')


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


# Add secret to existing user profile
@app.route('/entry/add', methods=['POST'])
def add_entry():

    error = None

    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':

        account = request.form.get('account', 'nick')
        username = request.form.get('username', 'nick')
        email = request.form.get('email', 'nicorellius@gmail.com')
        password = request.form.get('password', '123456')
        url = request.form.get('account_url', 'http://gmail.com')
        notes = request.form.get('notes', 'notes')

        print('this working?')

        print(account, username, email, password, url, notes)

        return redirect(url_for('home'))

    # data = {
    #     'error': error,
    # }

    # return render_template('manage.html', **data)


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

            # user = User(username='nicorellius', social_id='nicorellius')
            # user = User.objects(username='nick').upsert_one(
            #     set_on_insert__created=User().created,
            #     set__social_id='nick',
            #     upsert=True)

            user = User.objects(username='nick',
                                social_id='nick').modify(upsert=True, new=True,
                                                         set__username='nick',
                                                         set__social_id='nick')
            s = Secret(account_name='testing', login_string='nicorellius',
                       password=encrypt_string(
                           key_arn='arn:aws:kms:us-east-1:219595677748:key/22a160e7-839a-4ac1-a51f-393d685ee35c',
                           plaintext=secret),
                       url='http://example.com', notes='testing')

            logger.info('Encrypted secret: {0}'.format(s.password))
            user.passwords.append(s)
            # user.passwords.save()
            user.save()
            # print(s)

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

        user = User.objects.get(social_id=social_id)
        print('fetched user from database...')
        print('user: ' + user.username)

        config.logger.info('[{0}] Me in oauth_callback: {1}'.format(
            utils.get_timestamp(), user))

        # if user is None:
        #     print('no user...   ')
        #
        #     try:
        #         print('trying to create new user...')
        #         user =
        #             User(username=username, social_id=social_id, email=email)
        #         user.save()
        #
        #         config.logger.info('[{0}] New user created: {1}'.format(
        #             utils.get_timestamp(), user))
        #
        #     except ValueError:
        #         login_user(user, True)
        #         session['logged_in'] = True
        #         flash("Only one '{0}' can access this system.\n"
        #               "Logged in as 'guest' instead.".format(username),
        #               'notifications')
        #
        #         return redirect(url_for('home'))

        login_user(user, True)
        session['logged_in'] = True
        flash('You were logged in successfully', 'notifications')

        return redirect(url_for('home'))

    except TypeError as te:
        print("Seems something is wrong with provider's response")
        print('TypeError: {0}'.format(te))
        flash('Something went wrong... Authentication error', 'errors')

    return render_template('login.html')

