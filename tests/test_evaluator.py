import pytz

from datetime import datetime

from freezegun import freeze_time
from unittest import TestCase

from datetoken.evaluator import Datetoken
from datetoken.evaluator import localize, make_aware


class EvaluatorTestCase(TestCase):
    def test_eval_token_fluent_several_stages(self):
        now = datetime(2014, 11, 25, 23, 48, 43)
        now_minus_1d = datetime(2014, 11, 24, 23, 48, 43)
        datetok = Datetoken()
        datetok.at(now)
        datetok.on('Europe/Madrid')
        datetok.for_token('now/d')
        datetok.on('America/Chicago')
        datetok.at(now_minus_1d)
        datetok.for_token('now-d/d')
        then = datetok.to_date()
        self.assertEqual('America/Chicago', str(then.tzinfo))
        self.assertEqual(23, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)

    def test_eval_token_fluent_single(self):
        now = datetime(2014, 11, 25, 23, 48, 43)
        then = Datetoken().at(now).on(tz='Europe/Madrid')\
            .for_token('now/d').to_date()
        self.assertEqual(26, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)

    def test_eval_token_to_utc_date(self):
        utcnow = datetime(2014, 11, 2, 23, 48, 43)
        utc = pytz.UTC
        madrid = pytz.timezone('Europe/Madrid')
        payload = localize(make_aware(utcnow, utc), madrid)
        then = Datetoken(at=payload, token='now/d').to_utc_date()
        self.assertEqual(2, then.day)
        self.assertEqual(23, then.hour)
        self.assertEqual(00, then.minute)
        self.assertEqual(00, then.second)

    def test_eval_token_default_time_fallback_to_now_in_utc(self):
        """
        Datetoken defaults:
            - at: datetime.datetime.utcnow(..., tzinfo=UTC)
            - token: "now"
            - tz: None
        """
        frozen_time = datetime(2016, 11, 24, 23, 48, 43)
        expected = datetime(2016, 11, 24, 23, 48, 43)
        with freeze_time(frozen_time):
            expected = make_aware(expected, pytz.UTC)
            then = Datetoken().to_date()
            self.assertEqual(then, expected)

    def test_eval_token_tz_can_be_either_string_or_pytz_dot_timezone(self):
        # tz as string
        now = datetime(2014, 11, 25, 23, 48, 43)
        then = Datetoken(at=now, tz='Europe/Madrid', token='now/d').to_date()
        self.assertEqual(26, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)
        # Now as object
        then = Datetoken(at=now, tz=pytz.timezone('Europe/Madrid'),
                         token='now/d').to_date()
        self.assertEqual(26, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)

    def test_eval_token_with_naive_datetime_and_no_tz_coerce_to_utc(self):
        now = datetime(2014, 11, 25, 23, 48, 43)
        then = Datetoken(at=now, token='now/d').to_date()
        self.assertEqual(25, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)

    def test_eval_token_with_naive_datetime_and_tz_will_coerce_to_tz_from_utc(
            self):
        """
        Tests that prior to localization to Europe/Madrid, the datetime object
        had previously being casted to UTC, meaning that tzinfo was set to UTC
        only.
        """
        now = datetime(2014, 11, 25, 23, 48, 43)
        then = Datetoken(at=now, tz='Europe/Madrid', token='now/d').to_date()
        self.assertEqual(26, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)

    def test_eval_token_with_aware_datetime_and_no_tz_remains_untouched(self):
        utcnow = datetime(2014, 11, 25, 4, 48, 43)
        utc = pytz.UTC
        chicago = pytz.timezone('America/Chicago')
        payload = localize(make_aware(utcnow, utc), chicago)
        then = Datetoken(at=payload, token='now/d').to_date()
        self.assertEqual(24, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)

    def test_eval_token_with_naive_datetime_and_tz_being_utc_should_pass(self):
        now = datetime(2014, 11, 25, 4, 48, 43)
        then = Datetoken(at=now, tz=pytz.UTC, token='now/d').to_date()
        self.assertEqual(25, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)

    def test_eval_token_with_aware_datetime_and_tz_will_coerce_to_tz(self):
        utcnow = datetime(2014, 11, 25, 23, 48, 43)
        utc = pytz.UTC
        chicago = pytz.timezone('America/Chicago')
        # expected_localized = localize_naive(utcnow, 'America/Chicago',
        #                                     'Europe/Madrid')
        payload = localize(make_aware(utcnow, utc), chicago)
        then = Datetoken(at=payload, tz='Europe/Madrid',
                         token='now/d').to_date()
        self.assertEqual(26, then.day)
        self.assertEqual(0, then.hour)
        self.assertEqual(0, then.minute)
