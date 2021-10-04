import unittest

from datetoken.lexer import Lexer
from datetoken.token import TokenType


class TestLexer(unittest.TestCase):
    def test_illegal_token(self):
        token_input = "now*2h"
        lexer = Lexer(token_input)
        expected = (
            (TokenType.NOW, "now"),
            (TokenType.ILLEGAL, "*"),
            (TokenType.NUMBER, "2"),
            (TokenType.MODIFIER, "h"),
        )

        for exp_token_type, exp_token_literal in expected:
            actual_token = lexer.next_token()
            self.assertEqual(actual_token.token_type, exp_token_type)
            self.assertEqual(actual_token.token_literal, exp_token_literal)

    def test_next_token(self):
        token_input = "now-1h/h@M+2w/bw+2d/mon-3s-49d/m/tue@Y-wed/Y/Q/Q1/Q2/Q3/Q4"
        # token_input = 'now-1'
        expected = (
            (TokenType.NOW, "now"),
            (TokenType.MINUS, "-"),
            (TokenType.NUMBER, "1"),
            (TokenType.MODIFIER, "h"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "h"),
            (TokenType.AT, "@"),
            (TokenType.MODIFIER, "M"),
            (TokenType.PLUS, "+"),
            (TokenType.NUMBER, "2"),
            (TokenType.MODIFIER, "w"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "bw"),
            (TokenType.PLUS, "+"),
            (TokenType.NUMBER, "2"),
            (TokenType.MODIFIER, "d"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "mon"),
            (TokenType.MINUS, "-"),
            (TokenType.NUMBER, "3"),
            (TokenType.MODIFIER, "s"),
            (TokenType.MINUS, "-"),
            (TokenType.NUMBER, "49"),
            (TokenType.MODIFIER, "d"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "m"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "tue"),
            (TokenType.AT, "@"),
            (TokenType.MODIFIER, "Y"),
            (TokenType.MINUS, "-"),
            (TokenType.MODIFIER, "wed"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "Y"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "Q"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "Q1"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "Q2"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "Q3"),
            (TokenType.SLASH, "/"),
            (TokenType.MODIFIER, "Q4"),
            (TokenType.END, ""),
        )

        lexer = Lexer(token_input)

        for exp_token_type, exp_token_literal in expected:
            actual_token = lexer.next_token()
            self.assertEqual(actual_token.token_type, exp_token_type)
            self.assertEqual(actual_token.token_literal, exp_token_literal)
