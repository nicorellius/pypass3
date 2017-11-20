"""
PyPass3 Password Generator and Manager configuration
"""

import os
import string
import logging

# Secrets set here
# Flask application secret key
with open('/etc/prv/pypass/flask_secret_key.txt') as secret_key:
    FLASK_APP_SECRET_KEY = secret_key.read().strip()

# MongoDB database password
with open('/etc/prv/pypass/mongodb_password.txt') as mongodb_password:
    MONGO_DB_PASSWORD = mongodb_password.read().strip()

# RANDOM.ORG API Key
with open('/etc/prv/pypass/rdo_api_key.txt') as api_key:
    RDO_API_KEY = api_key.read().strip()

# CORE_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STATIC_PATH = os.path.join(PROJECT_ROOT, 'static')
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'templates')

# Word lists from EFF:
#     https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
#
# Local files
# WORDLIST_LONG = 'word_lists/wordlist_long.txt'
# WORDLIST_SHORT = 'word_lists/wordlist_short.txt'

# Remote files:
# https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
WORDLIST_LONG = 'http://bit.ly/2mtdxEk'
# https://www.eff.org/files/2016/09/08/eff_short_wordlist_2_0.txt
WORDLIST_SHORT = 'http://bit.ly/2ogvDGr'

# Note that this API key is not secure, and you should request your own!!!
API_KEY = RDO_API_KEY

_SPECIAL = '!@#$%^&*()_+=-?~'
CHARACTERS = '{ascii}{digits}{special}'.format(
    ascii=string.ascii_letters, digits=string.digits, special=_SPECIAL)

ROC_API_MAX_LENGTH = 20

appconf = dict(
    DEBUG=True,
    SECRET_KEY=FLASK_APP_SECRET_KEY,
    # Starting point for credentials
    USERNAME='guest',
    PASSWORD='password',
    # Debug Toolbar and MongoEngine configuration
    DEBUG_TB_INTERCEPT_REDIRECTS=False,
    DEBUG_TB_PANELS=[
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        'flask_mongoengine.panels.MongoDebugPanel',
    ],
    # Oauth configuration
    OAUTH_CREDENTIALS={
        'github': {
            'id': 'd3be9a39c8db65911ce0',
            'secret': 'cba32867fc777bd1291425e3aeedb222f51ef7c0'
        },
        'facebook': {
            'id': '137292646828195',
            'secret': 'e9ba084118895fc5dc82ed69eb6a3330'
        },
        'twitter': {
            'id': 'g3wINYT3Y3jI5iuxCFEJ5meG2',
            'secret': 'MH7c6kHwi7ICvyE0PyJl0Ezf7xJG7z15StmznMBG3TTcdE943p'
        },
        'google': {
            'id': '244230397026-m1t3fkrqmsgp1179igldfc8n3tgt0fhs.apps.googleusercontent.com',
            'secret': 'a4f9iIukFaLFj2DZMnkuqnV6'
        }
    },
    # Mongo configuration
    MONGODB_DB='pypass',
    MONGODB_ALIAS='core',
    MONGODB_HOST='localhost',
    MONGODB_PORT=27972,
    MONGODB_USERNAME='pypass',
    MONGODB_PASSWORD=MONGO_DB_PASSWORD,
)
