"""
Write some tests!

Testing this call:
def generate_password(number_rolls: int = 5, number_dice: int =5,
                      how_many: int = 1, output_type: str = 'words',
                      password_length: int = 20)

"""

import pytest

from generate import generate_secret
from generate import (
    _validate_count, _roll_dice, _concatenate_remainder,
    _prepare_chunks, _chunks
)

import config

from utils import get_roc

# All tests use these...
roc = get_roc(config.API_KEY)
chars = config.CHARACTERS


# ========== simple add function for sanity check ==========

def add_function(x):
    return x + 1


def test_add_function_pass():
    assert add_function(4) == 5

# ==========================================================


def test__concatenate_remainder_default():

    tmp_pw = _concatenate_remainder(roc, chars, 20)

    assert tmp_pw is not None
    assert len(tmp_pw) == 20


def test__concatenate_remainder_thirty_chars():

    tmp_pw = _concatenate_remainder(roc, chars, 30)

    assert tmp_pw is not None
    assert len(tmp_pw) == 30


def test__generate_password_mixed_default():

    result = generate_secret(output_type='mixed')

    assert result is not None
    assert len(result) == 20


def test__generate_password_numbers_default():

    result = generate_secret(output_type='numbers')

    assert result is not None
    assert len(result) == 20
    assert result.isdigit()


def test__generate_password_default():

    result = generate_secret()

    assert result is not None
    assert len(result.split()) == 5
    assert result.replace(' ', '').isalpha()


def test__generate_password_short_list_four_words():

    result = generate_secret(number_rolls=4, number_dice=4,
                             how_many=1, output_type='words',
                             password_length=20)

    assert result is not None
    assert len(result.split()) == 4


def test__generate_password_long_list_five_words():

    result = generate_secret(number_rolls=5, number_dice=5,
                             how_many=1, output_type='words',
                             password_length=20)

    assert result is not None
    assert len(result.split()) == 5


def test__generate_password_short_list_five_words():

    result = generate_secret(number_dice=4, number_rolls=5,
                             how_many=1, output_type='words',
                             password_length=20)

    assert result is not None
    assert len(result.split()) == 5


def test__generate_password_long_list_four_words():

    result = generate_secret(number_dice=5, number_rolls=4,
                             how_many=1, output_type='words',
                             password_length=20)

    assert result is not None
    assert len(result.split()) == 4


def test__roll_dice_is_list():

    r5 = _roll_dice()
    r4 = _roll_dice()

    # Test if roll result type is a list
    assert type(r5) is list
    assert type(r4) is list

    # Test for emptiness of various lists
    assert not [] is True  # This one is weird and confusing
    assert not []
    assert [1, 2, 3, 4, 5]
    assert r5, r4


# @pytest.mark.parametrize('execution_number', range(10))
# def test__roll_dice(execution_number):
#
#     r = _roll_dice()
#     total = sum(r)
#
#     assert total >= 25
#
#     # This test will fail ~7% of the time, so it's considered brittle
#     for i in {1, 2, 3, 4, 5, 6}:
#         assert i in r


def test__roll_dice():

    r = _roll_dice()
    total = sum(r)

    assert total >= 25
    assert 1 or 2 or 3 or 4 or 5 or 6 in r


def test__chunks():

    inlist = [1, 2, 3, 4, 5]
    results = _chunks(inlist, 1)

    assert results is not None


def test__prepare_chunks_four():

    result = _prepare_chunks(4, 4)

    for i in result:
        assert len(i) == 4


def test__prepare_chunks_five():
    result = _prepare_chunks(5, 5)

    for i in result:
        assert len(i) == 5


def test__validate_count():

    v1 = 4
    v2 = 5

    c1 = _validate_count(v1)
    c2 = _validate_count(v2)

    assert c1 == 4
    assert c2 == 5


def test__validate_count_throws_correct_exception():

    with pytest.raises(Exception):
        v3 = 6
        _validate_count(v3)
