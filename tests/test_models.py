import pytz
import unittest

from datetime import datetime
from freezegun import freeze_time

from datetoken.exceptions import InvalidTokenException
from datetoken.evaluator import eval_datetoken

frozen_time = datetime(2018, 12, 15, 10, 12, 34)


@freeze_time(frozen_time)
class TokenModelTestCase(unittest.TestCase):
    def compare_datetime(self, actual, expected):
        self.assertEqual(expected.year, actual.year)
        self.assertEqual(expected.month, actual.month)
        self.assertEqual(expected.day, actual.day)
        self.assertEqual(expected.hour, actual.hour)
        self.assertEqual(expected.minute, actual.minute)
        self.assertEqual(expected.second, actual.second)
        self.assertEqual(str(expected.tzinfo), str(actual.tzinfo))

    def eval_token(self, token):
        return eval_datetoken(token)

    def test_from_string_now(self):
        token = self.eval_token("now")
        self.assertFalse(token.is_calculated)
        self.assertFalse(token.is_snapped)
        self.assertEqual("now", str(token))
        self.compare_datetime(
            token.to_date(), datetime(2018, 12, 15, 10, 12, 34, tzinfo=pytz.UTC)
        )

    def test_invalid_from_string_should_raise(self):
        self.assertRaises(InvalidTokenException, self.eval_token, "now-1Z/a")

    def test_from_string_several_modifiers_are_parsed(self):
        token = self.eval_token("now-1d+2h/d")
        self.assertEqual("now-1d+2h/d", str(token))
        self.compare_datetime(
            token.to_date(), datetime(2018, 12, 14, 0, 0, 0, tzinfo=pytz.UTC)
        )

    def test_from_string_several_values_must_be_interpreted(self):
        payload = "now-1d+2h+1w/m"
        token = self.eval_token(payload)
        self.assertEqual(payload, str(token))
        self.compare_datetime(
            token.to_date(), datetime(2018, 12, 21, 12, 12, 00, tzinfo=pytz.UTC)
        )

    def test_now_token_is_optional(self):
        payload = "now-1d+2h+1w/m"
        token = self.eval_token(payload)
        self.assertEqual(payload, str(token))
        self.compare_datetime(
            token.to_date(), datetime(2018, 12, 21, 12, 12, 00, tzinfo=pytz.UTC)
        )
