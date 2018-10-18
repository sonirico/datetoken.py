import mock
import unittest

from datetoken import SNAP_ENDING
from datetoken.models import ComplexToken
from datetoken.models import SimpleToken

from .datetoken_testutils import NOW_MOCKED
from .datetoken_testutils import get_test_date


class SimpleTokenTestCase(unittest.TestCase):
    def setUp(self):
        self.default_token = SimpleToken()
        self.full_token = SimpleToken(1, 'd', '+', snap_to=SNAP_ENDING,
                                      snap_unit='h')

    def test_is_calculated_property(self):
        self.assertTrue(self.full_token.is_calculated)
        self.assertFalse(self.default_token.is_calculated)

    def test_is_snapped_property(self):
        self.assertTrue(self.full_token.is_snapped)
        self.assertFalse(self.default_token.is_snapped)

    def test_to_string_representation(self):
        self.assertEqual('now', str(self.default_token))
        self.assertEqual('now+1d@h', str(self.full_token))

    @mock.patch('datetoken.models.get_utc_now',
                return_value=NOW_MOCKED)
    def test_default_to_date_representation(self, *args):
        actual = self.default_token.to_date()
        expected = NOW_MOCKED
        self.assertEqual(expected, actual)

    @mock.patch('datetoken.models.get_utc_now',
                return_value=NOW_MOCKED)
    def test_full_token_to_date_representation(self, *args):
        actual = self.full_token.to_date()
        expected = get_test_date('2018-12-16 10:59:59')
        self.assertEqual(expected, actual)


class ComplexTokenTestCase(unittest.TestCase):
    def test_default_token(self):
        default_token = ComplexToken()
        self.assertFalse(default_token.is_calculated)
        self.assertFalse(default_token.is_snapped)
        self.assertEqual('now', str(default_token))

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            self.assertEqual(NOW_MOCKED, default_token.to_date())

    def test_complex_token_set_up(self):
        token_mods = [
            {
                'amount': 3,
                'unit': 'd',
                'sign': '+'
            },
            {
                'amount': 1,
                'unit': 'M',
                'sign': '-'
            }
        ]
        token = ComplexToken(values=token_mods, snap_to=SNAP_ENDING,
                             snap_unit='bw')
        self.assertTrue(token.is_calculated)
        self.assertTrue(token.is_snapped)
        self.assertEqual('now+3d-1M@bw', str(token))

        with mock.patch('datetoken.models.get_utc_now',
                        return_value=NOW_MOCKED):
            expected = get_test_date('2018-11-16 23:59:59')
            self.assertEqual(expected, token.to_date())


if __name__ == '__main__':
    unittest.main()
