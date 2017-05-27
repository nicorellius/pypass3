"""
Password Generator configuration
"""

import os
# import logging

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
CHARACTERS = 'abcdefghijklmnopqrstuvwxyz' \
             'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
             '1234567890!@#$%^&*()_+=-?~'

ROC_API_MAX_LENGTH = 20
