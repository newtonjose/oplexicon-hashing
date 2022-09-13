"""
General Purpose Hashing Functions in Python
Author: Ryan T. Dean
License: None
Github: https://github.com/rtdean/py-genhashlib
"""


MAX_INT = 0xffffffff
BITS_IN_INT = 8 * 4


def pjw(key: str) -> int:
    """
    An adaptation of Peter Weinberger's (PJW) generic hashing algorithm based on
    Allen Holub's version.  Accepts a string to be hashed and returns an integer
    :param key:
    :return:
    """
    assert isinstance(key, str), 'key: must be a string'
    three_quarters = int((BITS_IN_INT * 3) / 4)
    one_eighth = int(BITS_IN_INT / 8)
    high_bits = (MAX_INT << (BITS_IN_INT - one_eighth)) & MAX_INT
    hash_value = 0
    for char in key:
        hash_value = (hash_value << one_eighth) + ord(char)
        i = hash_value & 0xF0000000
        if i != 0:
            hash_value = (hash_value ^ (i >> three_quarters)) & ~high_bits
    return hash_value & 0x7fffffff
