"""
Password Generator configuration
"""

import os
import string

DEBUG = False

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Remote files:
# https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
WORDLIST_LONG = 'http://bit.ly/2mtdxEk'
# https://www.eff.org/files/2016/09/08/eff_short_wordlist_2_0.txt
WORDLIST_SHORT = 'http://bit.ly/2ogvDGr'

# Note that this API key is not secure, and you should request your own!!!
API_KEY = '59052bc4-840b-4923-96b7-90332167bc8c'

SPECIAL = '!@#$%^&*()_+=-?~'
CHARACTERS = '{0}{1}{2}'.format(string.ascii_letters, string.digits, SPECIAL)

ROC_API_MAX_LENGTH = 20
