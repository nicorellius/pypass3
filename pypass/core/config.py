"""
PyPass3 Password Generator and Manager configuration
"""

import os
import string
import logging

appconf = dict(
    DEBUG=True,
    SECRET_KEY='xN~@en@B%l0Kli6TBVUoxOP(tIJ_JnC@=9(a8N8cg27J)*nQ!c',
    # Starting point for credentials
    USERNAME='guest',
    PASSWORD='password',
    DEBUG_TB_INTERCEPT_REDIRECTS=False,
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
    MONGO_DBNAME='pypass',
    MONGO_PORT='12345',
    MONGO_USERNAME='pypass',
    MONGO_PASSWORD='gn5n_1xSb5ITqoKmG_oe',
)

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
API_KEY = '59052bc4-840b-4923-96b7-90332167bc8c'

_SPECIAL = '!@#$%^&*()_+=-?~'
CHARACTERS = '{ascii}{digits}{special}'.format(
    ascii=string.ascii_letters, digits=string.digits, special=_SPECIAL)

ROC_API_MAX_LENGTH = 20

# Set up logging configuration and get logger
# TODO: set up proper logging app with handler, formatter, etc...
logging.basicConfig(
    # filename='output.log',
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
