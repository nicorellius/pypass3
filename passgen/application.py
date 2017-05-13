"""
PyPass3

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Character 
Password Generator

Mozilla Public License Version 2
https://www.mozilla.org/en-US/MPL/2.0/

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

"""

from flask import (Flask, request, session, redirect,
                   url_for, abort, render_template, flash)

from flask_debugtoolbar import DebugToolbarExtension

from config import *
from generate import generate_password

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='xN~@en@B%l0Kli6TBVUoxOP(tIJ_JnC@=9(a8N8cg27J)*nQ!c',
    USERNAME='admin',
    PASSWORD='default',
    DEBUG_TB_INTERCEPT_REDIRECTS=False
))

app.config.from_envvar('PASSGEN_SETTINGS', silent=True)

app.debug = DEBUG
toolbar = DebugToolbarExtension(app)


@app.route('/')
def show_entries():

    # db = get_db()
    # cur = db.execute('select type, secret from entries order by id desc')
    # entries = cur.fetchall()

    return render_template('generate.html')  # , entries=entries)


@app.route('/generate', methods=['POST'])
def add_entry():

    if not session.get('logged_in'):
        abort(401)

    # db = get_db()
    # db.execute('insert into entries (type, secret) values (?, ?)',
    #            [request.form['type'], request.form['secret']])
    # db.commit()

    # output_type = request.form['type']
    output_type = request.form.get('type', 'words')
    # dice = int(request.form['dice'])
    dice = request.form.get('dice', 5)
    # rolls = int(request.form['rolls'])
    rolls = request.form.get('rolls', 5)
    # length = request.form['length'].strip()
    length = request.form.get('length', 20)
    num = 1

    if not length:  # type(length) is not int or
        length = 20
    else:
        length = int(length)

    if output_type is 'mixed' or 'numbers':
        dice, rolls = 5, 5

    print(output_type, dice, rolls, length, num)
    print(type(output_type), type(dice), type(rolls), type(length), type(num))

    try:
        secret = generate_password(number_rolls=rolls, number_dice=dice,
                                   how_many=num, output_type=output_type,
                                   password_length=length)
        flash(secret)
    except Exception as e:
        print(e)

    # flash('New entry was successfully posted')

    return redirect(url_for('show_entries'))


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
            return redirect(url_for('show_entries'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():

    session.pop('logged_in', None)
    flash('You were logged out')

    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
