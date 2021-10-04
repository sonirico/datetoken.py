import unittest

from datetoken.ast import NowExpression, ModifierExpression, SnapExpression
from datetoken.lexer import Lexer
from datetoken.parser import Parser
from datetoken.token import TokenType


class ParserExpression(unittest.TestCase):
    def check_expected_nodes(self, nodes, expected):
        for i, exp in enumerate(expected):
            node = nodes[i]
            if exp[0] == NowExpression:
                self.assertIsInstance(node, NowExpression)
            elif exp[0] == ModifierExpression:
                self.assertIsInstance(node, ModifierExpression)
                self.assertEqual(node.amount, exp[1])
                self.assertEqual(node.modifier, exp[2])
                self.assertEqual(node.operator, exp[3])
            elif exp[0] == SnapExpression:
                self.assertIsInstance(node, SnapExpression)
                self.assertEqual(node.operator, exp[1])
                self.assertEqual(node.modifier, exp[2])

    def test_parse_expression_base(self):
        lexer = Lexer("now-1h+w+2M/d+2d/thu-2s@m-5w@mon/Q1/Q")
        parser = Parser(lexer)
        nodes = parser.parse()
        expected = (
            (NowExpression, []),
            (ModifierExpression, 1, "h", "-"),
            (ModifierExpression, 1, "w", "+"),
            (ModifierExpression, 2, "M", "+"),
            (SnapExpression, TokenType.SLASH, "d"),
            (ModifierExpression, 2, "d", "+"),
            (SnapExpression, TokenType.SLASH, "thu"),
            (ModifierExpression, 2, "s", "-"),
            (SnapExpression, TokenType.AT, "m"),
            (ModifierExpression, 5, "w", "-"),
            (SnapExpression, TokenType.AT, "mon"),
            (SnapExpression, TokenType.SLASH, "Q1"),
            (SnapExpression, TokenType.SLASH, "Q"),
        )
        self.assertEqual(len(expected), len(nodes))
        self.check_expected_nodes(nodes, expected)

    def test_parse_expression_now_token_is_optional(self):
        lexer = Lexer("-1h+w+2M/d-2s@m")
        parser = Parser(lexer)
        nodes = parser.parse()
        self.assertEqual(6, len(nodes))
        expected = (
            (ModifierExpression, 1, "h", "-"),
            (ModifierExpression, 1, "w", "+"),
            (ModifierExpression, 2, "M", "+"),
            (SnapExpression, TokenType.SLASH, "d"),
            (ModifierExpression, 2, "s", "-"),
            (SnapExpression, TokenType.AT, "m"),
        )
        self.check_expected_nodes(nodes, expected)

    def test_parse_expression_catch_modified_literal_error_after_now(self):
        lexer = Lexer("now=1h+wx2M/d-2s@m")
        parser = Parser(lexer)
        parser.parse()
        error = parser.errors[0]
        self.assertIn('Illegal operator: "="', error)

    def test_parse_expression_catch_modified_literal_error(self):
        lexer = Lexer("now-1h+wxM/d-2s@m")
        parser = Parser(lexer)
        parser.parse()
        error = parser.errors[0]
        self.assertIn("Expected modifier literal", error)
        self.assertIn('got "wxM"', error)


class ParserNowExpression(unittest.TestCase):
    def test_alone_now(self):
        lexer = Lexer("now")
        parser = Parser(lexer)
        nodes = parser.parse()
        node = nodes[0]
        self.assertIsInstance(node, NowExpression)
        self.assertEqual("now", str(node))


class ParserSnapExpression(unittest.TestCase):
    def test_snap_non_existent_modifier(self):
        lexer = Lexer("@PEPE")
        parser = Parser(lexer)
        parser.parse()
        self.assertEqual(1, len(parser.errors))
        self.assertIn("Expected snap MODIFIER token type", parser.errors[0])

    def test_snap_ending(self):
        lexer = Lexer("@M")
        parser = Parser(lexer)
        nodes = parser.parse()
        node = nodes[0]
        self.assertIsInstance(node, SnapExpression)
        self.assertEqual(TokenType.AT, node.operator)
        self.assertEqual("M", node.modifier)
        self.assertEqual("@M", str(node))

    def test_snap_beginning(self):
        lexer = Lexer("/w")
        parser = Parser(lexer)
        nodes = parser.parse()
        node = nodes[0]
        self.assertIsInstance(node, SnapExpression)
        self.assertEqual(TokenType.SLASH, node.operator)
        self.assertEqual("w", node.modifier)
        self.assertEqual("/w", str(node))


class ParserModifierExpression(unittest.TestCase):
    def test_non_existent_operator(self):
        lexer = Lexer("*2m")
        parser = Parser(lexer)
        nodes = parser.parse()
        self.assertEqual(0, len(nodes))
        self.assertEqual(1, len(parser.errors))
        self.assertIn('Illegal operator: "*"', parser.errors[0])

    def test_amount_several_digits(self):
        lexer = Lexer("-99s")
        parser = Parser(lexer)
        nodes = parser.parse()
        node = nodes[0]
        self.assertIsInstance(node, ModifierExpression)
        self.assertEqual(99, node.amount)
        self.assertEqual("s", node.modifier)
        self.assertEqual("-", node.operator)

    def test_no_amount_defaults_to_1(self):
        lexer = Lexer("-m")
        parser = Parser(lexer)
        nodes = parser.parse()
        node = nodes[0]
        self.assertIsInstance(node, ModifierExpression)
        self.assertEqual(1, node.amount)
        self.assertEqual("m", node.modifier)
        self.assertEqual("-", node.operator)
