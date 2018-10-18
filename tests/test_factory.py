import mock
import unittest

from datetoken.exceptions import InvalidTokenException
from datetoken.factory import ComplexTokenFactory
from datetoken.factory import SimpleTokenFactory

from .datetoken_testutils import NOW_MOCKED
from .datetoken_testutils import get_test_date


class SimpleFactoryTestCase(unittest.TestCase):
    def test_from_string_now(self):
        token = SimpleTokenFactory.from_string('now')

        self.assertFalse(token.is_calculated)
        self.assertFalse(token.is_snapped)
        self.assertEqual('now', str(token))
        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            self.assertEqual(NOW_MOCKED, token.to_date())

    def test_invalid_from_string_should_raise(self):
        self.assertRaises(InvalidTokenException, SimpleTokenFactory.from_string,
                          'now-1Z/a')

    def test_from_string_several_modifiers_are_ignored_but_the_first(self):
        token = SimpleTokenFactory.from_string('now-1d+2h/d')
        self.assertEqual('now-1d/d', str(token))

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            expected = get_test_date('2018-12-14 00:00:00')
            self.assertEqual(expected, token.to_date())

    def test_from_dict(self):
        token = SimpleTokenFactory.from_dict({
            'values': [
                {
                    'amount': 3,
                    'unit': 'w',
                    'sign': '+'
                }
            ],
            'snap_to': None,
            'snap_unit': 'w'
        })

        self.assertEqual('now+3w', str(token))

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            expected = get_test_date('2019-01-05 10:12:34')
            self.assertEqual(expected, token.to_date())

    def test_from_dict_several_modifiers_are_ignored_but_the_first(self):
        token = SimpleTokenFactory.from_dict({
            'values': [
                {
                    'amount': 3,
                    'unit': 'w',
                    'sign': '+'
                },
                {
                    'amount': 1,
                    'unit': 'h',
                    'sign': '+'
                }
            ],
            'snap_to': None,
            'snap_unit': 'w'
        })

        self.assertEqual('now+3w', str(token))

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            expected = get_test_date('2019-01-05 10:12:34')
            self.assertEqual(expected, token.to_date())


class ComplexFactoryTestCase(unittest.TestCase):
    def test_from_string_now(self):
        token = ComplexTokenFactory.from_string('now')
        self.assertEqual('now', str(token))
        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            self.assertEqual(NOW_MOCKED, token.to_date())

    def test_from_string_several_values_must_be_interpreted(self):
        payload = 'now-1d+2h+1w/m'
        token = ComplexTokenFactory.from_string(payload)
        self.assertEqual(payload, str(token))
        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            expected = get_test_date('2018-12-21 12:12:00')
            self.assertEqual(expected, token.to_date())

    def test_from_dict(self):
        token = ComplexTokenFactory.from_dict({
            'values': [
                {
                    'amount': 3,
                    'unit': 'w',
                    'sign': '+'
                },
            ],
            'snap_to': None,
            'snap_unit': None
        })

        self.assertEqual('now+3w', str(token))

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            expected = get_test_date('2019-01-05 10:12:34')
            self.assertEqual(expected, token.to_date())

    def test_from_dict_several_modifiers_are_processed(self):
        token = ComplexTokenFactory.from_dict({
            'values': [
                {
                    'amount': 3,
                    'unit': 'w',
                    'sign': '+'
                },
                {
                    'amount': 1,
                    'unit': 'h',
                    'sign': '+'
                }
            ],
            'snap_to': None,
            'snap_unit': None
        })

        self.assertEqual('now+3w+1h', str(token))

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            expected = get_test_date('2019-01-05 11:12:34')
            self.assertEqual(expected, token.to_date())


if __name__ == '__main__':
    unittest.main()
