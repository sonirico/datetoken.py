from .models import Token


def token_to_date(token):
    """ Shortcut to rapidly get a datetime object from string tokens
    :param token:
    :return: datetime.datetime
    """
    return Token.from_string(token).to_date()
