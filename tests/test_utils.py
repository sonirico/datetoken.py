import pytz
import unittest

from datetime import datetime
from freezegun import freeze_time

from datetoken.exceptions import InvalidTokenException
from datetoken.utils import token_to_date, token_to_utc_date

frozen_time = datetime(2016, 11, 28, 12, 55, 23)


class DatetokenComparatorMixin(object):
    def compare_datetime(self, actual, expected):
        self.assertEqual(expected.year, actual.year)
        self.assertEqual(expected.month, actual.month)
        self.assertEqual(expected.day, actual.day)
        self.assertEqual(expected.hour, actual.hour)
        self.assertEqual(expected.minute, actual.minute)
        self.assertEqual(expected.second, actual.second)
        self.assertEqual(str(expected.tzinfo), str(actual.tzinfo))


@freeze_time(frozen_time)
class DateTokenToUTCDateTestCase(unittest.TestCase, DatetokenComparatorMixin):
    def test_default_token(self):
        payload = 'now'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_with_amount_modifiers(self):
        payload = 'now-5d+1h'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 23, 13, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_beginning_of_minute(self):
        payload = 'now/m'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 0,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_beginning_of_hour(self):
        payload = 'now/h'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 0, 0,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_beginning_of_day(self):
        payload = 'now/d'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 27, 23, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_week(self):
        payload = 'now/w'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2019, 2, 17, 23, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_month(self):
        payload = 'now/M'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2019, 1, 31, 23, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_year(self):
        payload = 'now/Y'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2018, 12, 31, 23, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_business_week(self):
        # TODO: bw is a highly relative concept ;)
        payload = 'now/bw'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2019, 2, 17, 23, 0, 0,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_minute(self):
        payload = 'now@m'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_hour(self):
        payload = 'now@h'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_day(self):
        payload = 'now@d'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 28, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_ending_of_week(self):
        payload = 'now@w'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2019, 2, 24, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_ending_of_business_week(self):
        payload = 'now@bw'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2019, 2, 22, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_month(self):
        payload = 'now@M'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 11, 30, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 12, 1, 0, 0, 0))
    def test_token_snapped_to_ending_of_month_edge_case_1(self):
        # Snap `now` to the beginning of the month
        payload = 'now@M'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2018, 12, 31, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 12, 31, 23, 59, 59))
    def test_token_snapped_to_ending_of_month_edge_case_2(self):
        # Snap `now` to the beginning of the month
        payload = 'now@M'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2019, 1, 31, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_year(self):
        payload = 'now@Y'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2016, 12, 31, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 1, 1, 0, 0, 0))
    def test_token_snapped_to_ending_of_year_edge_case_1(self):
        # Snap `now` to the beginning of the year
        payload = 'now@Y'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2018, 12, 31, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 12, 31, 23, 59, 59))
    def test_token_snapped_to_ending_of_year_edge_case_2(self):
        # Snap `now` to the ending of the year
        payload = 'now@Y'
        actual = token_to_utc_date(payload, tz='Europe/Madrid')
        self.compare_datetime(actual, datetime(2019, 12, 31, 22, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_invalid_string_should_raise(self):
        self.assertRaises(InvalidTokenException, token_to_utc_date,
                          'then-1d/d')
        self.assertRaises(InvalidTokenException, token_to_utc_date,
                          'now-1Z/d')


@freeze_time(frozen_time)
class DateTokenParseToDateTestCase(unittest.TestCase, DatetokenComparatorMixin):
    def test_default_token(self):
        payload = 'now'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_with_amount_modifiers(self):
        payload = 'now-5d+1h'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 23, 13, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_beginning_of_minute(self):
        payload = 'now/m'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 0,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_beginning_of_hour(self):
        payload = 'now/h'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 0, 0,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_beginning_of_day(self):
        payload = 'now/d'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 0, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_week(self):
        payload = 'now/w'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2019, 2, 18, 0, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_month(self):
        payload = 'now/M'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2019, 2, 1, 0, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_year(self):
        payload = 'now/Y'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2019, 1, 1, 0, 0, 0,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_beginning_of_business_week(self):
        # TODO: bw is a highly relative concept ;)
        payload = 'now/bw'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2019, 2, 18, 0, 0, 0,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_minute(self):
        payload = 'now@m'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_hour(self):
        payload = 'now@h'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_day(self):
        payload = 'now@d'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_ending_of_week(self):
        payload = 'now@w'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2019, 2, 24, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2019, 2, 20, 15, 45, 12))
    def test_token_snapped_to_ending_of_business_week(self):
        payload = 'now@bw'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2019, 2, 22, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_previous_friday(self):
        payload = 'now/fri'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 25, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_previous_sunday(self):
        payload = 'now/sun'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 27, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_prev_monday_yields_today(self):
        # Today is Monday. Therefore, should snap to today.
        payload = 'now/mon'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_following_friday(self):
        payload = 'now@fri'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 12, 2, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_following_sunday(self):
        payload = 'now@sun'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 12, 4, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_following_monday(self):
        # Today is Saturday. Therefore, should snap to today.
        payload = 'now@mon'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 28, 12, 55, 23,
                                               tzinfo=pytz.UTC))

    def test_day_of_week_token_can_be_combined_1(self):
        payload = 'now@sun/d'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 12, 4, 0, 0, 0,
                                               tzinfo=pytz.UTC))

    def test_day_of_week_token_can_be_combined_2(self):
        payload = 'now/sun@d'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 27, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_month(self):
        payload = 'now@M'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 11, 30, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 12, 1, 0, 0, 0))
    def test_token_snapped_to_ending_of_month_edge_case_1(self):
        # Snap `now` to the beginning of the month
        payload = 'now@M'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2018, 12, 31, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 12, 31, 23, 59, 59))
    def test_token_snapped_to_ending_of_month_edge_case_2(self):
        # Snap `now` to the beginning of the month
        payload = 'now@M'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2018, 12, 31, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_token_snapped_to_ending_of_year(self):
        payload = 'now@Y'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2016, 12, 31, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 12, 1, 0, 0, 0))
    def test_token_snapped_to_ending_of_year_edge_case_1(self):
        # Snap `now` to the beginning of the year
        payload = 'now@Y'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2018, 12, 31, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    @freeze_time(datetime(2018, 12, 31, 23, 59, 59))
    def test_token_snapped_to_ending_of_year_edge_case_2(self):
        # Snap `now` to the ending of the year
        payload = 'now@Y'
        actual = token_to_date(payload)
        self.compare_datetime(actual, datetime(2018, 12, 31, 23, 59, 59,
                                               tzinfo=pytz.UTC))

    def test_invalid_string_should_raise(self):
        self.assertRaises(InvalidTokenException, token_to_date,
                          'then-1d/d')
        self.assertRaises(InvalidTokenException, token_to_date,
                          'now-1Z/d')


if __name__ == '__main__':
    unittest.main()
