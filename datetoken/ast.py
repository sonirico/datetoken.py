import abc
import pytz

from datetime import timedelta as td
from datetime import datetime

from dateutil.relativedelta import relativedelta

from datetoken.token import TokenType


def get_utc_now():
    """
    :rtype: datetime.datetime
    :return: Timezone aware datetime object in UTC
    """
    now = datetime.utcnow()
    now = now.replace(microsecond=0)
    now = pytz.UTC.localize(now)
    if hasattr(pytz.UTC, 'normalize'):
        now = pytz.UTC.normalize(now)
    return now


class Expression(object):
    @abc.abstractmethod
    def get_value(self, *args):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass


class NowExpression(Expression):
    """
    Dummy expression used to represent the existence of the
    optional part `now` within a token. Only returns back
    whatever it gets, acting as an identity expression.
    """
    def get_value(self, value):
        return value

    def __str__(self):
        return "now"


class ModifierExpression(Expression):
    __operations__ = {
        TokenType.PLUS: {
            "s": lambda dt, amount: dt + td(seconds=amount),
            "m": lambda dt, amount: dt + td(minutes=amount),
            "h": lambda dt, amount: dt + td(hours=amount),
            "d": lambda dt, amount: dt + td(days=amount),
            "w": lambda dt, amount: dt + td(weeks=amount),
            "M": lambda dt, amount: dt + relativedelta(months=amount),
        },
        TokenType.MINUS: {
            "s": lambda dt, amount: dt - td(seconds=amount),
            "m": lambda dt, amount: dt - td(minutes=amount),
            "h": lambda dt, amount: dt - td(hours=amount),
            "d": lambda dt, amount: dt - td(days=amount),
            "w": lambda dt, amount: dt - td(weeks=amount),
            "M": lambda dt, amount: dt - relativedelta(months=amount),
        },
    }

    def __init__(self, amount, modifier, operator):
        self.amount = amount
        self.modifier = modifier
        self.operator = operator

    def get_value(self, value):
        fn = self.__operations__[self.operator][self.modifier]
        return fn(value, self.amount)

    def __str__(self):
        return "%s%s%s" % (
            self.operator,
            self.amount,
            self.modifier,
        )


class SnapExpression(Expression):
    __operations__ = {
        TokenType.SLASH: {
            "s": lambda dt: dt.replace(second=0),
            "m": lambda dt: dt.replace(second=0),
            "h": lambda dt: dt.replace(minute=0, second=0),
            "d": lambda dt: dt.replace(
                hour=0, minute=0, second=0
            ),
            "w": lambda dt: (
                dt - td(days=dt.weekday())
            ).replace(hour=0, minute=0, second=0),
            "M": lambda dt: dt.replace(
                day=1, hour=0, minute=0, second=0
            ),
            "bw": lambda dt: (
                dt - td(days=dt.weekday())
            ).replace(hour=0, minute=0, second=0),
        },
        TokenType.AT: {
            "s": lambda dt: dt.replace(
                second=0, millisecond=999
            ),
            "m": lambda dt: dt.replace(second=59),
            "h": lambda dt: dt.replace(
                minute=59, second=59
            ),
            "d": lambda dt: dt.replace(
                hour=23, minute=59, second=59
            ),
            "w": lambda dt: (
                dt - td(days=dt.weekday()) + td(days=6)
            ).replace(hour=23, minute=59, second=59),
            "M": lambda dt: (
                dt + relativedelta(months=1, days=-dt.day)
            ).replace(hour=23, minute=59, second=59),
            "bw": lambda dt: (
                dt - td(days=dt.weekday()) + td(days=4)
            ).replace(hour=23, minute=59, second=59),
        },
    }

    def __init__(self, modifier, operator):
        self.operator = operator
        self.modifier = modifier

    def get_value(self, value):
        fn = self.__operations__[self.operator][
            self.modifier
        ]
        return fn(value)

    def __str__(self):
        return self.operator + self.modifier
