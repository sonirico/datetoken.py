from .__operations__ import TokenOperations, get_utc_now
from .factory import SimpleTokenFactory
from .factory import ComplexTokenFactory
from .parser import token_to_dict


def simple_token_to_date(token):
    """ Parses tokens reading zero or one amount modifiers

    :param token: string token representation
    :return: datetime token representation
    :rtype: datetime.datetime
    :raises: InvalidTokenException
    """

    token_model = SimpleTokenFactory.from_string(token)
    return token_model.to_date()


def complex_token_to_date(token):
    """ Parses tokens reading all amount modifiers

    :param token: string token representation
    :return: datetime token representation
    :rtype: datetime.datetime
    :raises: InvalidTokenException
    """

    token_model = ComplexTokenFactory.from_string(token)
    return token_model.to_date()


def token_to_date(token):
    """ Provides a generic, model agnostic and fast token normalization

    :param token: token as string
    :return: datetime representation
    :rtype: datetime.datetime
    :raises: InvalidTokenException
    """
    token_model = token_to_dict(token)
    result = get_utc_now()

    amount_modifiers = token_model['values']

    if amount_modifiers:
        for amount_mod in amount_modifiers:
            sign = amount_mod['sign']
            unit = amount_mod['unit']
            # Retrieve the amount modifier function
            amount_mod_func = TokenOperations.get_amount_modifier(sign, unit)
            result = amount_mod_func(result, amount_mod['amount'])

    snap_to = token_model['snap_to']
    snap_unit = token_model['snap_unit']

    if snap_to and snap_unit:
        snap_mod_func = TokenOperations.get_snap_modifier(snap_to, snap_unit)
        result = snap_mod_func(result)

    return result
