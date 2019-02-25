from .evaluator import Datetoken


def token_to_date(token=None, **kwargs):
    """ Shortcut to rapidly get a datetime object from string tokens
    :return: datetime.datetime
    """
    return Datetoken(token=token, **kwargs).to_date()


def token_to_utc_date(token=None, **kwargs):
    return Datetoken(token, **kwargs).to_utc_date()
