import pytz
from datetime import datetime

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
NOW_MOCKED = datetime.strptime('2018-12-15 10:12:34', DATETIME_FORMAT) \
    .replace(tzinfo=pytz.UTC)


def get_test_date(date_str, fmt=DATETIME_FORMAT):
    # Helper function to assist testing by creating datetime
    # objects from string
    return datetime.strptime(date_str, fmt).replace(tzinfo=pytz.UTC)
