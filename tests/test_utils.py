import mock
import unittest

from datetoken.exceptions import InvalidTokenException
from datetoken.utils import complex_token_to_date
from datetoken.utils import token_to_date
from datetoken.utils import simple_token_to_date

from .datetoken_testutils import NOW_MOCKED
from .datetoken_testutils import get_test_date


@mock.patch('datetoken.utils.get_utc_now', return_value=NOW_MOCKED)
class DateTokenParseToDateTestCase(unittest.TestCase):
    def test_default_token(self, *args):
        payload = 'now'
        actual = token_to_date(payload)
        expected = NOW_MOCKED

        self.assertEqual(expected, actual)

    def test_token_with_amount_modifiers(self, *args):
        payload = 'now-5d+1h'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-10 11:12:34')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_beginning_of_minute(self, *args):
        payload = 'now/m'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-15 10:12:00')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_beginning_of_hour(self, *args):
        payload = 'now/h'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-15 10:00:00')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_beginning_of_day(self, *args):
        payload = 'now/d'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-15 00:00:00')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_beginning_of_week(self, *args):
        payload = 'now/w'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-10 00:00:00')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_beginning_of_month(self, *args):
        payload = 'now/M'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-01 00:00:00')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_beginning_of_business_week(self, *args):
        payload = 'now/bw'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-10 00:00:00')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_minute(self, *args):
        payload = 'now@m'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-15 10:12:59')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_hour(self, *args):
        payload = 'now@h'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-15 10:59:59')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_day(self, *args):
        payload = 'now@d'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-15 23:59:59')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_week(self, *args):
        payload = 'now@w'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-16 23:59:59')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_business_week(self, *args):
        payload = 'now@bw'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-14 23:59:59')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_month(self, *args):
        payload = 'now@M'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-31 23:59:59')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_month_edge_case_1(self, mocked, *args):
        # Snap `now` to the beginning of the month
        mocked.return_value = get_test_date('2018-12-01 00:00:00')
        payload = 'now@M'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-31 23:59:59')
        self.assertEqual(expected, actual)

    def test_token_snapped_to_ending_of_month_edge_case_2(self, mocked, *args):
        # Snap `now` to the beginning of the month
        mocked.return_value = get_test_date('2018-12-31 23:59:59')
        payload = 'now@M'
        actual = token_to_date(payload)
        expected = get_test_date('2018-12-31 23:59:59')
        self.assertEqual(expected, actual)


class SimpleTokenToDateUtilTestCase(unittest.TestCase):
    """ This test case should remain as simpler as possible since utils
        only work as proxies for other functionality, tested already.
    """
    def test_invalid_string_should_raise(self):
        self.assertRaises(InvalidTokenException, simple_token_to_date,
                          'then-1d/d')
        self.assertRaises(InvalidTokenException, simple_token_to_date,
                          'now-1Z/d')

    def test_correct_token_should_pass(self, *args):
        payload = 'now/d'

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            actual = simple_token_to_date(payload)
            expected = get_test_date('2018-12-15 00:00:00')
            self.assertEqual(expected, actual)


class ComplexTokenToDateUtilTestCase(unittest.TestCase):
    """ This test case should remain as simpler as possible since utils
        only work as proxies for other functionality, tested already.
    """
    def test_invalid_string_should_raise(self):
        self.assertRaises(InvalidTokenException, complex_token_to_date,
                          'then-1d/d')
        self.assertRaises(InvalidTokenException, complex_token_to_date,
                          'now-1Z/d')

    def test_complex_token(self):
        payload = 'now-M+d-h/d'

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            actual = simple_token_to_date(payload)
            expected = get_test_date('2018-11-15 00:00:00')
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
