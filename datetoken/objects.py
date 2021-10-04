from functools import reduce

from .ast import get_utc_now
from .ast import NowExpression, ModifierExpression, SnapExpression


class Token(object):
    def __init__(self, nodes=None, at=None):
        self._at = at
        if not nodes:
            self._nodes = [NowExpression()]
        elif not isinstance(nodes[0], NowExpression):
            self._nodes = nodes
            self._nodes.insert(0, NowExpression())
        else:
            self._nodes = nodes

    @property
    def is_snapped(self):
        """
        :rtype: bool
        :return: Whether the token has been snapped, either to the beginning
            or end.
        """
        return any((isinstance(node, SnapExpression) for node in self._nodes))

    @property
    def is_calculated(self):
        """
        :rtype: bool
        :return: Whether the token is modified, meaning it suffers from
            additions or subtractions.
        """
        return any((isinstance(node, ModifierExpression) for node in self._nodes))

    def refresh_at(self, new_at=None):
        self._at = new_at or get_utc_now()

    @property
    def at(self):
        return self._at

    def to_date(self):
        """
        Evaluate ast nodes sequentially, starting with the current
        value of `_at`
        :return:
        """
        return reduce(
            lambda accumulated, node: node.get_value(accumulated), self._nodes, self._at
        )

    def __str__(self):
        return "".join([str(node) for node in self._nodes])
