import pytz

from datetime import datetime
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta

from . import SNAP_ENDING, SNAP_BEGINNING


class TokenOperations(object):
    """ This class wraps operations over dates providing a couple of
        methods to access modifying/snapping functions cleanly
    """
    __OPERATIONS__ = {
        "+": {
            "s": lambda dt, amount: dt + td(seconds=amount),
            "m": lambda dt, amount: dt + td(minutes=amount),
            "h": lambda dt, amount: dt + td(hours=amount),
            "d": lambda dt, amount: dt + td(days=amount),
            "w": lambda dt, amount: dt + td(weeks=amount),
            "M": lambda dt, amount: dt + relativedelta(months=amount),
        },
        "-": {
            "s": lambda dt, amount: dt - td(seconds=amount),
            "m": lambda dt, amount: dt - td(minutes=amount),
            "h": lambda dt, amount: dt - td(hours=amount),
            "d": lambda dt, amount: dt - td(days=amount),
            "w": lambda dt, amount: dt - td(weeks=amount),
            "M": lambda dt, amount: dt - relativedelta(months=amount),
        },
        SNAP_BEGINNING: {
            "s": lambda dt: dt.replace(second=0),
            "m": lambda dt: dt.replace(second=0),
            "h": lambda dt: dt.replace(minute=0, second=0),
            "d": lambda dt: dt.replace(hour=0, minute=0, second=0),
            "w": lambda dt: (dt - td(days=dt.weekday())).replace(
                hour=0, minute=0, second=0
            ),
            "M": lambda dt: dt.replace(day=1, hour=0, minute=0, second=0),
            "bw": lambda dt: (dt - td(days=dt.weekday())).replace(
                hour=0, minute=0, second=0
            ),
        },
        SNAP_ENDING: {
            "s": lambda dt: dt.replace(second=0, millisecond=999),
            "m": lambda dt: dt.replace(second=59),
            "h": lambda dt: dt.replace(minute=59, second=59),
            "d": lambda dt: dt.replace(hour=23, minute=59, second=59),
            "w": lambda dt: (dt - td(days=dt.weekday()) + td(days=6)).replace(
                hour=23, minute=59, second=59
            ),
            "M": lambda dt: (
                dt + relativedelta(months=1, days=-dt.day)
            ).replace(hour=23, minute=59, second=59),
            "bw": lambda dt: (dt - td(days=dt.weekday()) + td(days=4)).replace(
                hour=23, minute=59, second=59
            ),
        },
    }

    @classmethod
    def get_amount_modifier(cls, sign, unit):
        return cls.__OPERATIONS__[sign][unit]

    @classmethod
    def get_snap_modifier(cls, snap_to, snap_unit):
        return cls.__OPERATIONS__[snap_to][snap_unit]


def get_utc_now():
    """
    :rtype: datetime.datetime
    :return: Timezone aware datetime object in UTC
    """
    return datetime.utcnow().replace(tzinfo=pytz.UTC, microsecond=0)
