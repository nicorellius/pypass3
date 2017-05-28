"""
PyPass3

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Character 
Password Generator

Mozilla Public License Version 2
https://www.mozilla.org/en-US/MPL/2.0/

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

"""
import logging

from flask import (Flask, request, session, redirect,
                   url_for, abort, render_template, flash)

import utils
import config

from csrf import csrf
from generate import generate_secret

app = Flask(__name__)

# Protect with CSRF
csrf(app)

app.config.from_object(__name__)
app.config.from_envvar('PYPASS_SETTINGS', silent=True)

app.debug = config.DEBUG

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='xN~@en@B%l0Kli6TBVUoxOP(tIJ_JnC@=9(a8N8cg27J)*nQ!c',
    USERNAME='admin',
    PASSWORD='default',
    DEBUG_TB_INTERCEPT_REDIRECTS=False,
))

if app.debug is True:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)

logging.basicConfig(
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)


@app.route('/')
def home():

    return render_template('generate.html')


@app.route('/generate', methods=['POST'])
def generate():

    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':

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
                flash("UUID can be a maximum of 32 characters")

            elif length == 32:
                secret = utils.gen_uid()
                flash(secret)

            else:
                secret = utils.gen_uid(length, True)
                flash(secret)

            return redirect(url_for('home'))

        try:
            secret = generate_secret(number_rolls=int(rolls),
                                     number_dice=int(dice),
                                     how_many=num,
                                     output_type=str(output_type),
                                     secret_length=length)

            flash(secret)

            _log_output_params(output_type, dice, rolls, length, num)

            return redirect(url_for('home'))

        except Exception as e:
            print("Exception: {0}".format(e))


@app.route('/settings')
def settings():

    if request.method == 'POST':

        return redirect(url_for('home'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'

        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'

        else:

            session['logged_in'] = True

            flash('You were logged in')
            return redirect(url_for('home'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():

    session.pop('logged_in', None)
    flash('You were logged out')

    return redirect(url_for('login'))


def _log_output_params(output_type, dice, rolls, length, num):

    return logging.info(
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


if __name__ == '__main__':
    app.run()
