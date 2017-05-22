"""
PyPass3

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Character 
Password Generator

Mozilla Public License Version 2
https://www.mozilla.org/en-US/MPL/2.0/

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

"""
import logging

from collections import namedtuple

from flask import (Flask, request, session, redirect,
                   url_for, abort, render_template, flash)

from flask_debugtoolbar import DebugToolbarExtension
from flask_pymongo import PyMongo

import utils
import config

from generate import generate_password

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='xN~@en@B%l0Kli6TBVUoxOP(tIJ_JnC@=9(a8N8cg27J)*nQ!c',
    USERNAME='admin',
    PASSWORD='default',
    DEBUG_TB_INTERCEPT_REDIRECTS=False,
))

# mongo db setup
# TODO: set envars for these secrets
# TODO: figure out why these can't belong to the config.update above
# app.config['MONGO_DBNAME'] = 'pypass'
# app.config['MONGO_PORT'] = '12345'
# app.config['MONGO_USERNAME'] = 'pypass'
# app.config['MONGO_PASSWORD'] = 'gn5n_1xSb5ITqoKmG_oe'
#
# mongo = PyMongo(app)

app.config.from_envvar('PYPASS_SETTINGS', silent=True)

app.debug = config.DEBUG
toolbar = DebugToolbarExtension(app)


# Set up logging configuration
# TODO: set up proper logging app with handler, formatter, etc...
logging.basicConfig(
    # filename='output.log',
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)

persist_results = None


@app.route('/')
def home():

    # secrets = mongo.db.secret_collection.find_one()
    return render_template('generate.html')  # , secrets=secrets)


@app.route('/generate', methods=['POST'])
def generate_secret():

    global persist_results

    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':

        # TODO: figure out why request.form.get(value, default) only works
        # TODO: for the radio buttons... not a field for request.form['field']?

        # TODO: figure out how to validate form input
        output_type = request.form.get('type', 'words')
        dice = request.form.get('dice', 5)
        rolls = request.form.get('rolls', 5)
        # TODO: check out generate.py line 93, gives warning in console:
        # TODO: '<=' not supported between instances of 'str' and 'int'
        length = request.form.get('length', 20)
        num = 1

        submit = request.form['submit']

        logging.info('[{0}] Button pressed: {1}'.format(
            utils.get_timestamp(), submit))

        Results = namedtuple('Results', 'rolls, dice, num, output, length,')
        persist_results = Results(rolls, dice, num, output_type, length)

        logging.info('[{0}] Form data: {1}'.format(
            utils.get_timestamp(), persist_results))

        # collection = mongo.db.form_data_collection
        # r = {'form_set_data': persist_results}
        # r_id = collection.insert_one(r).inserted_id

        # logging.info('[{0}] Collection ID: {1}'.format(
        #     utils.get_timestamp(), r_id))

        if request.form['submit'] == 'Run Again':

            try:
                secret = generate_password(
                    number_rolls=int(persist_results.rolls),
                    number_dice=int(persist_results.dice),
                    how_many=persist_results.num,
                    output_type=str(persist_results.output),
                    password_length=persist_results.length
                )

                # flash(utils.crypto_hash(secret))

                collection = mongo.db.secret_collection
                s = {'secret': secret}
                s_id = collection.insert_one(s).inserted_id

                logging.info('[{0}] Collection ID: {1}'.format(
                    utils.get_timestamp(), s_id))

                flash(secret)

                _log_output_params(output_type, dice, rolls, length, num)

                return redirect(url_for('home'))

            except Exception as e:
                print(e)
        else:
            pass

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
            secret = generate_password(number_rolls=int(rolls),
                                       number_dice=int(dice),
                                       how_many=num,
                                       output_type=str(output_type),
                                       password_length=length)

            # flash(utils.crypto_hash(
            #     secret,
            #     'K1vGZPsxgd6SEmkpD?xIG-g_8-GnIC!8)EPzk_=45chrNE%51g')
            # )

            flash(secret)

            _log_output_params(output_type, dice, rolls, length, num)

            return redirect(url_for('home'))

        except Exception as e:
            print(e)


@app.route('/settings')
def settings():

    if request.method == 'POST':

        return redirect(url_for('home'))

    return render_template('settings.html')


# @app.route('/settings/save', methods=['POST'])
# def save_settings():
#     pass


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


if __name__ == '__main__':
    app.run()


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
