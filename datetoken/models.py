from functools import reduce

from .ast import NowExpression, ModifierExpression, SnapExpression
from .exceptions import InvalidTokenException
from .parser import Parser
from .lexer import Lexer


class Token(object):
    @classmethod
    def from_string(cls, input_token):
        lexer = Lexer(input_token)
        parser = Parser(lexer)
        nodes = parser.parse()
        if not nodes:
            raise InvalidTokenException(lexer.input)
        if parser.errors:
            raise InvalidTokenException(lexer.input, errors=parser.errors)
        return Token(nodes)

    def __init__(self, nodes=None):
        if not nodes:
            self.nodes = [NowExpression()]
        elif not isinstance(nodes[0], NowExpression):
            self.nodes = nodes
            self.nodes.insert(0, NowExpression())
        else:
            self.nodes = nodes

    @property
    def is_snapped(self):
        """
        :rtype: bool
        :return: Whether the token has been snapped, either to the beginning
            or end.
        """
        return any([isinstance(node, SnapExpression) for node in self.nodes])

    @property
    def is_calculated(self):
        """
        :rtype: bool
        :return: Whether the token is modified, meaning it suffers from
            additions or subtractions.
        """
        return any(
            [isinstance(node, ModifierExpression) for node in self.nodes])

    def to_date(self):
        return reduce(lambda accumulated, node: node.get_value(accumulated),
                      self.nodes, None)

    def __str__(self):
        return ''.join([str(node) for node in self.nodes])
