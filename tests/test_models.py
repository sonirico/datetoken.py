import mock
import unittest


from datetoken.exceptions import InvalidTokenException
from datetoken.models import Token

from .datetoken_testutils import NOW_MOCKED
from .datetoken_testutils import get_test_date


@mock.patch('datetoken.ast.get_utc_now', return_value=NOW_MOCKED)
class TokenModelTestCase(unittest.TestCase):
    def test_from_string_now(self, *args):
        token = Token.from_string('now')

        self.assertFalse(token.is_calculated)
        self.assertFalse(token.is_snapped)
        self.assertEqual('now', str(token))
        self.assertEqual(NOW_MOCKED, token.to_date())

    def test_invalid_from_string_should_raise(self, *args):
        self.assertRaises(InvalidTokenException, Token.from_string,
                          'now-1Z/a')

    def test_from_string_several_modifiers_are_parsed(self, *args):
        token = Token.from_string('now-1d+2h/d')
        self.assertEqual('now-1d+2h/d', str(token))
        expected = get_test_date('2018-12-14 00:00:00')
        self.assertEqual(expected, token.to_date())

    def test_from_string_several_values_must_be_interpreted(self, *args):
        payload = 'now-1d+2h+1w/m'
        token = Token.from_string(payload)
        self.assertEqual(payload, str(token))
        expected = get_test_date('2018-12-21 12:12:00')
        self.assertEqual(expected, token.to_date())

    def test_now_token_is_optional(self, *args):
        payload = '-1d+2h+1w/m'
        token = Token.from_string(payload)
        self.assertEqual('now' + payload, str(token))
        expected = get_test_date('2018-12-21 12:12:00')
        self.assertEqual(expected, token.to_date())
