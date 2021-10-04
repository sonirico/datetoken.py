import pytz
import six

from . import DEFAULT_TOKEN
from .ast import get_utc_now
from .exceptions import InvalidTokenException
from .lexer import Lexer
from .objects import Token
from .parser import Parser


def is_naive(dt):
    """
    :param dt: datetime.datetime
    :return: Whether datetime is tz unaware
    """
    return dt.utcoffset() is None


def is_aware(dt):
    """
    :param dt: datetime.datetime
    :return: Whether datetime is tz aware
    """
    return not is_naive(dt)


def make_aware(datetime_obj, tz):
    """
    Set `tzinfo` attr to naive datetime objects
    :param datetime_obj:
    :param tz:
    :return:
    :raises: ValueError is datetime is already aware
    """
    if hasattr(tz, "localize"):
        return tz.localize(datetime_obj)
    if is_aware(datetime_obj):
        raise ValueError("Expected a naive datetime")
    return datetime_obj.replace(tzinfo=tz)


def localize(datetime_obj, tz):
    """
    Localize tz aware datetime objects to the target time zone
    :param datetime_obj:
    :param tz:
    :return:
    :raises: ValueError is datetime object is naive. Coercion can
        only be applied when the source tz and destination are both
        known
    """
    if is_naive(datetime_obj):
        raise ValueError("Cannot localize naive datetime")
    localized = datetime_obj.astimezone(tz)
    if hasattr(tz, "normalize"):
        return tz.normalize(localized)
    return localized


def localize_naive(datetime_obj, tz_from, tz_to):
    """
    Coerce a naive datetime to a given tz an apply the destination time zone
    over it
    :param datetime_obj:
    :param tz_from: origin tz
    :param tz_to: target tz
    :return: Aware datetime object
    """
    tz_s = pytz.timezone(tz_from)
    tz_d = pytz.timezone(tz_to)
    aware_datetime = make_aware(datetime_obj, tz_s)
    return localize(aware_datetime, tz_d)


def eval_datetoken(token, **kwargs):
    """
    Evaluates a token
    :param token:
    :param kwargs:
        - at: {datetime.datetime} starting point or, `now`'s value in other
            words
        - tz: {str|pytz.timezone} a pytz object or their string repr.
    :return: datetoken.object structure that carries token meta-information
    """
    now = kwargs.get("at") or get_utc_now()
    tz_name = kwargs.get("tz")
    tz = pytz.timezone(tz_name) if isinstance(tz_name, six.string_types) else tz_name
    # Coerce tz unaware tokens to UTC as default behaviour
    if is_naive(now):
        now = make_aware(now, pytz.UTC)
    if tz:
        now = localize(now, tz)

    lexer = Lexer(token)
    parser = Parser(lexer)
    ast_nodes = parser.parse()

    if not ast_nodes:
        raise InvalidTokenException(lexer.input)
    if parser.errors:
        raise InvalidTokenException(lexer.input, errors=parser.errors)
    return Token(ast_nodes, at=now)


class Datetoken(object):
    """
    Util middleware to fluently configure and evaluate
    tokens. Configuration options are:
    - TZ: defaults to UTC
    - now: defaults to datetime.datetime.utcnow
    """

    def __init__(self, at=None, tz=None, token=DEFAULT_TOKEN):
        self._at = at
        self._tz = tz
        self._token = token
        self._result = None

    @property
    def object(self):
        return self._result

    def for_token(self, token=DEFAULT_TOKEN):
        """
        Set the token
        :param token:
        :return:
        """
        self._token = token
        return self

    def on(self, tz):
        """
        Set the time zone
        :param tz: Time zone name
        :return:
        """
        self._tz = tz
        return self

    def at(self, at):
        """
        Set the starting point in time
        :param at: datetime. Can be localized already
        :return:
        """
        self._at = at
        return self

    def eval(self, token=None):
        """
        Evaluates and keep the result
        :param token: Date token
        :return:
        """
        if token:
            self._token = token

        self._result = eval_datetoken(self._token, at=self._at, tz=self._tz)
        return self

    def to_date(self):
        """
        Retrieves the datetime object corresponding to the
        already evaluated token
        :return:
        """
        if not self._result:
            self.eval()
        return self._result.to_date()

    def to_utc_date(self):
        """
        Retrieves the datetime object corresponding to the
        whole evaluated token, localized to UTC.
        :return:
        """
        result = self.to_date()
        if result.tzinfo is not None and result.tzinfo == pytz.UTC:
            return result

        return localize(result, pytz.UTC)
