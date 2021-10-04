from .ast import (
    NowExpression,
    ModifierExpression,
    SnapExpression,
)
from .token import TokenType

AMOUNT_MODIFIERS = ("s", "m", "h", "d", "w", "M", "Y")
SNAP_MODIFIERS = (
    "s",
    "m",
    "h",
    "d",
    "w",
    "bw",
    "M",
    "Y",
    "mon",
    "tue",
    "wed",
    "thu",
    "fri",
    "sat",
    "sun",
    "Q",
    "Q1",
    "Q2",
    "Q3",
    "Q4",
)


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.peek_token = None
        self.current_token = None

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_expression(self):
        tt = self.current_token.token_type
        if TokenType.NOW == tt:
            return self.parse_now_expression()
        elif TokenType.PLUS == tt or TokenType.MINUS == tt:
            return self.parse_modifier_expression()
        elif TokenType.SLASH == tt or TokenType.AT == tt:
            return self.parse_snap_expression()
        elif TokenType.ILLEGAL == tt:
            self.errors.append(
                'Illegal operator: "%s"' % self.current_token.token_literal
            )
            return None
        return None

    def parse_now_expression(self):
        return NowExpression()

    def parse_modifier_expression(self):
        operator = self.current_token.token_literal
        self.next_token()
        amount = 1
        if self.current_token.token_type == TokenType.NUMBER:
            amount = int(self.current_token.token_literal)
            self.next_token()
        if self.current_token.token_type == TokenType.MODIFIER:
            modifier = self.current_token.token_literal
            if modifier not in AMOUNT_MODIFIERS:
                self.errors.append(
                    'Expected modifier literal as any of "%s", got "%s"'
                    % (AMOUNT_MODIFIERS, modifier)
                )
            return ModifierExpression(amount, modifier, operator)
        else:
            self.errors.append(
                'Expected NUMBER or MODIFIER token type, got "%s"'
                % self.current_token.token_type
            )

    def parse_snap_expression(self):
        operator = self.current_token.token_literal
        self.next_token()
        if self.current_token.token_type != TokenType.MODIFIER:
            self.errors.append(
                'Expected amount MODIFIER token type, got "%s"'
                % self.current_token.token_type
            )
        modifier = self.current_token.token_literal
        if modifier not in SNAP_MODIFIERS:
            self.errors.append(
                'Expected snap MODIFIER token type, got "%s", choices are "%s"'
                % (modifier, str(SNAP_MODIFIERS))
            )
        return SnapExpression(modifier, operator)

    def parse(self):
        nodes = []
        self.next_token()
        self.next_token()
        while self.current_token.token_type is not TokenType.END:
            node = self.parse_expression()
            if not node:
                break
            nodes.append(node)
            self.next_token()
        return nodes
