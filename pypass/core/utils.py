import binascii
import datetime
import hashlib
import os
import random
import re
import uuid
import logging

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rdoclient import RandomOrgClient

# this likely results in circular
# from ..apps.generate import generate_secret

from . import config


logger = logging.getLogger('pypass')


# get time in format I like
def get_timestamp():
    """
    Function to generate timestamp for use in application

    :return timestamp:
    """

    dt = datetime.datetime.now()

    return dt.strftime("%Y-%m-%d %X")


def log_output_params(output_type, dice, rolls, length, num):

    return logger.info(
        'Parameters:\n'
        '        output type: {0} {1}\n'
        '     number of dice: {2}      {3}\n'
        '    number of rolls: {4}      {5}\n'
        '      secret length: {6}     {7}\n'
        '  number of secrets: {8}      {9}'.format(
            output_type, type(output_type),
            dice, type(dice),
            rolls, type(rolls),
            length, type(length),
            num, type(num))
    )


def gen_uid(length=10, rid=False):
    """
    Function to generate random id of varying length for application

    :param length: length of uid
    :param rid: random ID
    :return uid: formatted string
    """

    # TODO - find one that works in both v2.x/3.x...
    # python 3.x version
    uid = uuid.uuid4()

    if rid is False:
        return uid

    else:
        tmp_uid = re.sub('-', '', str(uid))

    return ''.join(random.sample(list(tmp_uid), length))


# TODO: this function is not ready for show time. Experimental only!
# TODO: Use Argon2 instead for hashing passwords
def hash_password(password, salt_length=16,
                  iterations=10000, encoding='utf-8'):
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
    return binascii.hexlify(hashed_password)

    # Bytes version
    # return hashed_password


# TODO: this function is not ready for show time. Experimental only!
# TODO: Use Argon2 instead for hashing passwords
def crypto_hash(secret, salt='tTn0ICSQ8d!pVGULB+L='):

    """
    Hash routine for securing secrets

    :param secret: 
    :param salt:
    :return: encoded hashed secret
    """

    backend = default_backend()

    if not salt or len(salt) < 10:
        os.urandom(16)  # this calls OS random generator
        # salt = generate_secret(output_type='mixed', secret_length=20)

    salt = bytes(salt, 'utf-8')

    # now = time.clock()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32, salt=salt, iterations=1000000,
                     backend=backend)

    key = kdf.derive(bytes(secret, 'utf-8'))

    # print(key)

    kdf2 = PBKDF2HMAC(algorithm=hashes.SHA256(),
                      length=32, salt=salt, iterations=100000,
                      backend=backend)

    verify = kdf2.verify(bytes(secret, 'utf-8'), key)

    return verify


def get_roc(api_key=config.RDO_API_KEY):
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


def encrypt(secret):
    """
    Encrypt secret and return it

    :param secret
    :return: key and encrypted secret
    """

    key = Fernet.generate_key()
    f = Fernet(key)
    ciphertext = f.encrypt(bytes(secret, 'utf-8'))

    return ciphertext


def decrypt(key, token):
    """
    Decrypt token (ciphertext) and return it

    :param token: ciphertext
    :param key
    :return: decrypted secret
    """

    f = Fernet(key)
    secret = f.decrypt(token)

    return secret


def sha3_hash(message):
    """
    Hash message with SHA3-512

    :param message:
    :return: SHA3-512 hash
    """

    return hashlib.sha3_512(message)
