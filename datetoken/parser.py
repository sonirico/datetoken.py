import re

from . import AMOUNT_PATTERN
from . import TOKEN_PATTERN
from . import SNAP_BEGINNING
from . import SNAP_ENDING
from . import SNAP_PATTERN

from .exceptions import InvalidTokenException


def token_to_dict(token):
    """ Receives a string representation of a relative date and returns
        a json like object, with the following structure

        {
            "values": [
                {
                    "amount": 1,
                    "unit": "h",
                    "sign": "+"
                },
                ...
            ],
            "snap_to": "/",
            "snap_unit": "bw"
        }

    :param token: string representation of a token
    :return: dict with parsed data
    :rtype: dict
    :raises: InvalidTokenException
    """

    # First of all, perform a total validation
    if re.search(TOKEN_PATTERN, token) is None:
        raise InvalidTokenException(token)

    result = {'values': [], 'snap_to': None, 'snap_unit': None}

    # Look for amount modifiers
    has_additions = '+' in token
    has_subtractions = '-' in token

    if has_additions or has_subtractions:
        result['values'] = [
            {
                'sign': match[0],
                'amount': int((match[1] or 1)),  # The absence of amount
                # defaults to 1
                'unit': match[2]
            }
            for match in re.findall(AMOUNT_PATTERN, token)
        ]

    # Look for snaps
    snapped_from = SNAP_BEGINNING in token
    snapped_to = SNAP_ENDING in token

    if snapped_from or snapped_to:
        matches = re.search(SNAP_PATTERN, token).groupdict()
        result['snap_to'] = matches['snap_to']
        result['snap_unit'] = matches['snap_unit']

    return result
