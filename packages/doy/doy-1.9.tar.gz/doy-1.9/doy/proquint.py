# adapted from https://github.com/dsw/proquint/tree/master
import random


def _char_list_to_dict(char_list):
    return {c: k for (c, k) in zip(char_list, range(len(char_list)))}

UINT_TO_CONSONANT = "bdfghjklmnprstvz"
UINT_TO_VOWEL = "aiou"

CONSONANT_TO_UINT = _char_list_to_dict(UINT_TO_CONSONANT)
VOWEL_TO_UINT = _char_list_to_dict(UINT_TO_VOWEL)

MASK_LAST4 = 0xF
MASK_LAST2 = 0x3

CHARS_PER_CHUNK = 5

def _uint16_to_quint(uint16_val):
    val = uint16_val
    res = ["?"] * CHARS_PER_CHUNK
    for i in range(CHARS_PER_CHUNK):
        if i & 1:
            res[-i - 1] = UINT_TO_VOWEL[val & MASK_LAST2]
            val >>= 2
        else:
            res[-i - 1] = UINT_TO_CONSONANT[val & MASK_LAST4]
            val >>= 4
    return "".join(res)


def uint2quint(uint_val, separator="-"):
    """Convert 32-bit integer value into corresponding proquint string identifier.

    >>> uint2quint(0x7F000001, '-')
    lusab-babad

    :param uint_val: 32-bit integer value to encode
    :param separator: string to separate character quintets
    :return: proquint string identifier
    """
    if uint_val < 0 or uint_val > 0xFFFFFFFF:
        raise ValueError("uint_val should be in range 0-0xFFFFFFFF")
    return _uint16_to_quint(uint_val >> 16) + separator + _uint16_to_quint(uint_val)

def random_proquint(n=1, sep="-"):
    """ Generate a random proquint with n*16 bits of entropy."""
    res = [_uint16_to_quint(random.getrandbits(16)) for _ in range(n)]
    return sep.join(res)