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
    if hasattr(pytz.UTC, "normalize"):
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
            "Y": lambda dt, amount: dt + relativedelta(years=amount),
        },
        TokenType.MINUS: {
            "s": lambda dt, amount: dt - td(seconds=amount),
            "m": lambda dt, amount: dt - td(minutes=amount),
            "h": lambda dt, amount: dt - td(hours=amount),
            "d": lambda dt, amount: dt - td(days=amount),
            "w": lambda dt, amount: dt - td(weeks=amount),
            "M": lambda dt, amount: dt - relativedelta(months=amount),
            "Y": lambda dt, amount: dt - relativedelta(years=amount),
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


def start_current_quarter(dt):
    q = (dt.month - 1) // 3
    return start_quarter(dt, q)


def start_quarter(dt, q):
    return dt.replace(month=q * 3 + 1, day=1, hour=0, minute=0, second=0)


def create_start_quarter(q):
    return lambda dt: start_quarter(dt, q)


def end_current_quarter(dt):
    q = (dt.month - 1) // 3
    return end_quarter(dt, q)


def end_quarter(dt, q):
    d = 30 if q in (1, 2) else 31
    return dt.replace(month=q * 3 + 3, day=d, hour=23, minute=59, second=59)


def create_end_quarter(q):
    return lambda dt: end_quarter(dt, q)


class SnapExpression(Expression):
    __operations__ = {
        TokenType.SLASH: {
            "s": lambda dt: dt.replace(second=0),
            "m": lambda dt: dt.replace(second=0),
            "h": lambda dt: dt.replace(minute=0, second=0),
            "d": lambda dt: dt.replace(hour=0, minute=0, second=0),
            "w": lambda dt: (dt - td(days=dt.weekday())).replace(
                hour=0, minute=0, second=0
            ),
            "M": lambda dt: dt.replace(day=1, hour=0, minute=0, second=0),
            "Y": lambda dt: dt.replace(month=1, day=1, hour=0, minute=0, second=0),
            "bw": lambda dt: (dt - td(days=dt.weekday())).replace(
                hour=0, minute=0, second=0
            ),
            "mon": lambda dt: (dt - td(days=dt.weekday())),
            "tue": lambda dt: (dt - td(days=((dt.weekday() - 1) % 7))),
            "wed": lambda dt: (dt - td(days=((dt.weekday() - 2) % 7))),
            "thu": lambda dt: (dt - td(days=((dt.weekday() - 3) % 7))),
            "fri": lambda dt: (dt - td(days=((dt.weekday() - 4) % 7))),
            "sat": lambda dt: (dt - td(days=((dt.weekday() - 5) % 7))),
            "sun": lambda dt: (dt - td(days=((dt.weekday() - 6) % 7))),
            "Q": start_current_quarter,
            "Q1": create_start_quarter(0),
            "Q2": create_start_quarter(1),
            "Q3": create_start_quarter(2),
            "Q4": create_start_quarter(3),
        },
        TokenType.AT: {
            "s": lambda dt: dt.replace(second=0, millisecond=999),
            "m": lambda dt: dt.replace(second=59),
            "h": lambda dt: dt.replace(minute=59, second=59),
            "d": lambda dt: dt.replace(hour=23, minute=59, second=59),
            "w": lambda dt: (dt - td(days=dt.weekday()) + td(days=6)).replace(
                hour=23, minute=59, second=59
            ),
            "M": lambda dt: (dt + relativedelta(months=1, days=-dt.day)).replace(
                hour=23, minute=59, second=59
            ),
            "Y": (
                lambda dt: dt.replace(
                    year=dt.year + 1,
                    month=1,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                )
                - relativedelta(seconds=1)
            ),
            "bw": lambda dt: (dt - td(days=dt.weekday()) + td(days=4)).replace(
                hour=23, minute=59, second=59
            ),
            "mon": lambda dt: (dt + td(days=((0 - dt.weekday()) % 7))),
            "tue": lambda dt: (dt + td(days=((1 - dt.weekday()) % 7))),
            "wed": lambda dt: (dt + td(days=((2 - dt.weekday()) % 7))),
            "thu": lambda dt: (dt + td(days=((3 - dt.weekday()) % 7))),
            "fri": lambda dt: (dt + td(days=((4 - dt.weekday()) % 7))),
            "sat": lambda dt: (dt + td(days=((5 - dt.weekday()) % 7))),
            "sun": lambda dt: (dt + td(days=((6 - dt.weekday()) % 7))),
            "Q": end_current_quarter,
            "Q1": create_end_quarter(0),
            "Q2": create_end_quarter(1),
            "Q3": create_end_quarter(2),
            "Q4": create_end_quarter(3),
        },
    }

    def __init__(self, modifier, operator):
        self.operator = operator
        self.modifier = modifier

    def get_value(self, value):
        fn = self.__operations__[self.operator][self.modifier]
        return fn(value)

    def __str__(self):
        return self.operator + self.modifier
