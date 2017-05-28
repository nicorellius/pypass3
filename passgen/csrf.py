# -*- coding: utf-8 -*-
"""
A small Flask extension for adding CSRF protection.

Copyright (c) 2010 Steve Losh

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import string

from flask import abort, request, session, g
from werkzeug.routing import NotFound

from generate import generate_secret


_exempt_views = []


def csrf_exempt(view):

    _exempt_views.append(view)

    return view


def csrf(app, on_csrf=None):

    @app.before_request
    def _csrf_check_exemptions():

        try:
            dest = app.view_functions.get(request.endpoint)
            g._csrf_exempt = dest in _exempt_views

        except NotFound:
            g._csrf_exempt = False

    @app.before_request
    def _csrf_protect():

        # This simplifies unit testing, wherein CSRF seems to break
        if app.config.get('TESTING'):
            return

        if not g._csrf_exempt:
            if request.method == "POST":
                csrf_token = session.pop('_csrf_token', None)
                if not csrf_token or csrf_token != request.form.get('_csrf_token'):
                    if on_csrf:
                        on_csrf(*app.match_request())
                    abort(400)

    def generate_csrf_token():

        chars = string.ascii_letters + string.digits

        if '_csrf_token' not in session:
            session['_csrf_token'] = generate_secret(5, 5, 1,
                                                     'mixed', 50, chars)

        return session['_csrf_token']

    app.jinja_env.globals['csrf_token'] = generate_csrf_token
