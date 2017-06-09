"""
Password Generator configuration
"""

import os
import string
import logging

DEBUG = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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

SPECIAL = '!@#$%^&*()_+=-?~'
CHARACTERS = '{0}{1}{2}'.format(string.ascii_letters, string.digits, SPECIAL)

# CHARACTERS = 'abcdefghijklmnopqrstuvwxyz' \
#              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
#              '1234567890!@#$%^&*()_+=-?~'

ROC_API_MAX_LENGTH = 20

# Set up logging configuration and get logger
# TODO: set up proper logging app with handler, formatter, etc...
logging.basicConfig(
    # filename='output.log',
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)

# Example usage for this application:
#   logger.info('[{0}] Log message, {1}, goes here'.format(
#       utils.get_timestamp(), name2)
#   )

logger = logging.getLogger(__name__)
