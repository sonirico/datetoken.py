import unittest

from datetoken import SNAP_BEGINNING
from datetoken import SNAP_ENDING
from datetoken.exceptions import InvalidTokenException
from datetoken.parser import token_to_dict


class DateTokenParseToDictTestCase(unittest.TestCase):
    def test_token_default(self):
        payload = 'now'
        actual = token_to_dict(payload)
        expected = {
            'values': [],
            'snap_to': None,
            'snap_unit': None
        }
        self.assertDictEqual(expected, actual)

    def test_token_with_modifier(self):
        payload = 'now-1d'
        actual = token_to_dict(payload)
        expected = {
            'snap_unit': None,
            'snap_to': None,
            'values': [
                {
                    'amount': 1,
                    'unit': 'd',
                    'sign': '-'
                }
            ]
        }
        self.assertDictEqual(expected, actual)

    def test_token_snapped_to_beginning(self):
        payload = 'now/d'
        actual = token_to_dict(payload)
        expected = {
            'snap_unit': 'd',
            'snap_to': SNAP_BEGINNING,
            'values': []
        }
        self.assertDictEqual(expected, actual)

    def test_token_snapped_to_ending(self):
        payload = 'now@d'
        actual = token_to_dict(payload)
        expected = {
            'snap_unit': 'd',
            'snap_to': SNAP_ENDING,
            'values': []
        }
        self.assertEqual(expected, actual)

    def test_token_with_several_amount_modifiers_and_snapped(self):
        payload = 'now-1w+3h-2s@m'
        actual = token_to_dict(payload)
        expected = {
            'snap_to': SNAP_ENDING,
            'snap_unit': 'm',
            'values': [
                {
                    'amount': 1,
                    'unit': 'w',
                    'sign': '-',
                },
                {
                    'amount': 3,
                    'unit': 'h',
                    'sign': '+',
                },
                {
                    'amount': 2,
                    'unit': 's',
                    'sign': '-',
                }
            ]
        }
        self.assertEqual(expected, actual)

    def test_invalid_token_should_raise(self):
        payload = 'now-2A-zZ/T'
        self.assertRaises(InvalidTokenException, token_to_dict, payload)


if __name__ == '__main__':
    unittest.main()
