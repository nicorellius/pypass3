import os
import re
import random
import hashlib
# import binascii
import datetime
import uuid

from rdoclient import RandomOrgClient

import config


# get time in format I like
def get_timestamp():
    """
    Function to generate timestamp for use in application

    :return timestamp:
    """

    dt = datetime.datetime.now()

    return dt.strftime("%Y-%m-%d %X")


def gen_uid(length=10):
    """
    Function to generate random uuid of varying length for application

    :param length: length of uid
    :return uid: formatted string
    """

    # TODO - find one that works in both v2.x/3.x...
    # python 3.x version
    uid = uuid.uuid4()

    tmp_uid = re.sub('-', '', str(uid))

    return ''.join(random.sample(list(tmp_uid), length))


def hash_password(password, salt_length=16, iterations=1000000, encoding='utf-8'):
    """
    Function to securely hash password with variable salt and iterations
    :param password: input secret
    :param salt_length: length of salt
    :param iterations: number of times to cycle this algorithm
    :param encoding: character encoding
    :return: hashed password
    """

    salt = os.urandom(salt_length)

    hashed_password = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=bytes(password, encoding),
        salt=salt,
        iterations=iterations,
    )

    # Non-bytes version
    # return binascii.hexlify(hashed_password)
    # Bytes version
    return hashed_password


def get_roc(api_key=config.API_KEY):
    """
    Get instance of RandomOrgClient for testing.

    :param api_key: API key to fetch API client
    :return: instance of ROC
    """

    try:
        roc = RandomOrgClient(api_key)
        return roc

    except (ValueError, AttributeError) as e:
        print(e)
