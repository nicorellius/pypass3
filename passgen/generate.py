#!/usr/bin/env python

"""
PyPass3

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Character 
Password Generator

Mozilla Public License Version 2
https://www.mozilla.org/en-US/MPL/2.0/

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

"""

import logging

from urllib import request
from urllib.error import HTTPError

import utils
import config


# Set up logging configuration
# TODO: set up proper logging app with handler, formatter, etc...
logging.basicConfig(
    # filename='output.log',
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)


def generate_secret(number_rolls: int = 5, number_dice: int =5,
                    how_many: int = 1, output_type: str = 'words',
                    password_length: int = 20):
    """
    Generate a password or passphrase with either random characters,
    words, or numbers. Optionally, choose number of dice rolls
    for passphrase word selection. See https://www.eff.org/dice.

    \n
    Returns unencrypted passphrase or password (output type).

    \b
    Available arguments:
        how_many: how many passwords do you want
        output_type: words, mixed, numbers
        number_rolls: (optional) how many times you want to roll the dice
        number_dice: (optional) how many dice you want to roll
        password_length: (optional) length of output type
    """

    # TODO: number of rolls = number of words
    # TODO: number of dice determine which word list

    chars = config.CHARACTERS
    factor = 1
    api_max_length = config.ROC_API_MAX_LENGTH
    result = []
    roc = utils.get_roc()

    if output_type == 'words':

        if number_dice == 4:
            word_list = config.WORDLIST_SHORT
            logging.info(
                '[{0}] Using short word list...'.format(utils.get_timestamp()))
        else:
            word_list = config.WORDLIST_LONG
            logging.info(
                '[{0}] Using long word list...'.format(utils.get_timestamp()))

        chunked_list = _prepare_chunks(number_rolls, number_dice)
        result, password_length = _match_numbers_words(word_list, chunked_list)

    elif output_type == 'numbers':
        chars = '1234567890'

        logging.info(
            '[{0}] Output type `numbers` selected...'.format(
                utils.get_timestamp())
        )

    else:
        logging.info(
            '[{0}] Output type `mixed` selected...'.format(
                utils.get_timestamp())
        )

    if output_type != 'words':

        if password_length <= 20:
            result = ''.join(roc.generate_strings(factor * how_many,
                                                  password_length, chars))
        elif password_length > 20:
            result = _concatenate_remainder(roc, chars, password_length,
                                            how_many, api_max_length)
    else:
        result = result

    logging.info('[{0}] Your password is: {1}'.format(
        utils.get_timestamp(), result)
    )

    return result


def _match_numbers_words(wd_list, ch_list):
    """
    Match numbers from dice rolls to word list.
    
    :param wd_list: word list
    :param ch_list: chunked lists of numbers for dice rolls
    :return: passphrase and length
    """

    # Initialize list, dict, and empty passphrase
    password_length = 0
    super_list = []
    super_dict = {}
    passphrase = ''

    try:
        # TODO: Refactor to accept local word lists
        # with open(word_list, 'r') as words:
        #     lines = words.readlines()
        #     for line in lines:

        for line in request.urlopen(wd_list):
            # Take word list and break apart into list
            l = line.decode()
            d = {int(l.split('\t')[0]): l.split('\t')[1].strip('\n')}
            super_list.append(d)

    except HTTPError as e:
        logging.error('[{0}] {1}'.format(utils.get_timestamp(), e))

    # Convert list into str and int components
    for k in set(k for d in super_list for k in d):
        for d in super_list:
            if k in d:
                super_dict[k] = d[k]

    # Extract the int per roll and map to words for passphrase
    for chunk in ch_list:
        n = int(''.join(map(str, chunk)))
        passphrase += '{0} '.format(super_dict[n])

    return passphrase, password_length


def _prepare_chunks(number_rolls, number_dice):

    number_list = _roll_dice(number_rolls, number_dice)
    number_dice = _validate_count(number_dice)
    chunks = list(_chunks(number_list, number_dice))

    if config.DEBUG is True:
        logging.info('[{0}] Chunked list:\n  {1}'.format(
            utils.get_timestamp(), chunks)
        )

    return chunks


def _concatenate_remainder(roc, chars, pw_len,
                           how_many=1, max_length=20):
    """
    API limitation is 20 character string, so if CLI input is longer
    than 20 characters, we must concatenate the string and reminder string.

    :param roc: instance of RandomOrgClient
    :param chars: character set to use for making secret
    :param pw_len: length of output (password)
    :param how_many: how many passwords do you want
    :param max_length: maximum default length, API imposed
    :return: concatenated string
    """

    remainder_str, factor_str = '', ''

    # TODO: why int is required in outer scope?
    factor = pw_len // 20  # old version was factor = int(pw_len) // 20
    remainder = pw_len % 20  # old version was factor = int(pw_len) % 20

    if config.DEBUG:
        logging.info(
            '[{0}] factor: {1}, remainder: {2}'.format(
                utils.get_timestamp(), factor, remainder)
        )

    # Generate string in length equal to remainder
    if pw_len > 20:
        if remainder == 0:
            remainder_str = ''
        else:
            remainder_str = ''.join(roc.generate_strings(how_many,
                                                         remainder, chars))

    # Multiply factor by how_many to get multiple strings
    factor_str = ''.join(roc.generate_strings(factor * how_many,
                                              max_length, chars))

    # Build the concatenated string and return it
    return '{0}{1}'.format(remainder_str, factor_str)


def _roll_dice(number_rolls=5, number_dice=5, number_sides=6):
    """
    Get some randomness using random.org API: https://api.random.org

    :param number_sides: choose a die type and number of sides
    :param number_rolls: how many rolls determines how long your password is
    :param number_dice: how many dice do you want to roll
    :return: string, concatenated numbers (consider list?)
    """

    try:
        roc = utils.get_roc()
        return roc.generate_integers(number_rolls * number_dice, 1,
                                     number_sides)
    except (ValueError, AttributeError) as e:
        print(e)


def _chunks(input_list, size):

    """Yield successive n-sized chunks from input_list.
    
    :param input_list: list you want to chunk
    :param size: size of chunks
    """

    for i in range(0, len(input_list), size):
        yield input_list[i:i + size]


def _validate_count(value):
    """
    Validate that count is 4 or 5, because EFF lists
    only work for these number of dice.

    :param value: value to validate
    :return: value after it's validated
    """

    # Use `set` ({x, y, z}) here for quickest result
    if value not in {4, 5}:
        raise ValueError(
            'Words in word lists limit number of dice to 4 or 5.'
        )

    return value


# Main call to command line function
if __name__ == '__main__':
    generate_secret()
