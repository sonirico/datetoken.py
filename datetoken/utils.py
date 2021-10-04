from .evaluator import Datetoken


def token_to_date(token=None, **kwargs):
    """Shortcut to rapidly get a datetime object from string tokens
    :return: datetime.datetime
    """
    return Datetoken(token=token, **kwargs).to_date()


def token_to_utc_date(token=None, **kwargs):
    """
    Quickly evaluate a token and coerce it back to UTC
    :param token: string payload
    :param kwargs:
        - at: datetime.datetime
        - tz: string or pytz.timezone
    :return:
    """
    return Datetoken(token=token, **kwargs).to_utc_date()
