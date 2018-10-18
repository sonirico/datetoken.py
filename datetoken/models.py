from abc import ABCMeta, abstractmethod
from abc import abstractproperty  # In P3 properties and abstract methods can
# be nested

from . import NOW
from .__operations__ import TokenOperations, get_utc_now


class Token(object):
    __metaclass__ = ABCMeta

    def __init__(self, snap_to=None, snap_unit=None, **kwargs):
        self.snap_to = snap_to
        self.snap_unit = snap_unit

    @property
    def is_snapped(self):
        """
        :rtype: bool
        :return: Whether the token has been snapped, either to the beginning
            or end.
        """
        return self.snap_to is not None and self.snap_unit is not None

    @abstractproperty
    def is_calculated(self):
        """
        :rtype: bool
        :return: Whether the token is modified, meaning it suffers from
            additions or subtractions.
        """
        raise NotImplementedError

    @abstractmethod
    def to_date(self):
        """
        :rtype: datetime.datetime
        :return: datetime representation
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError


class SimpleToken(Token):
    """ A simple token that only takes in account zero or one modifiers, thus
        leveraging memory by ignoring all but the first modifiers. Handy for
        simple usage where the user only works with a limited preset of tokens
    """
    def __init__(self, amount=None, unit=None, sign=None, **kwargs):
        self.sign = sign
        self.amount = amount
        self.unit = unit

        super(SimpleToken, self).__init__(**kwargs)

    @property
    def is_calculated(self):
        return self.amount is not None and self.unit is not None

    def to_date(self):
        result = get_utc_now()

        if self.is_calculated:
            amount_mod_func = TokenOperations.get_amount_modifier(self.sign,
                                                                  self.unit)
            result = amount_mod_func(result, self.amount)

        if self.is_snapped:
            amount_mod_func = TokenOperations.get_snap_modifier(self.snap_to,
                                                                self.snap_unit)
            result = amount_mod_func(result)

        return result

    def __str__(self):
        res = NOW
        if self.is_calculated:
            res += '{}{}{}'.format(self.sign, self.amount, self.unit)
        if self.is_snapped:
            res += '{}{}'.format(self.snap_to, self.snap_unit)
        return res


class ComplexToken(Token):
    """ Parses all amount modifiers. It should be only used in advanced usage
        modes.
    """
    def __init__(self, **kwargs):
        self.values = kwargs.pop('values', [])

        super(ComplexToken, self).__init__(**kwargs)

    @property
    def is_calculated(self):
        return len(self.values) > 0

    def to_date(self):
        result = get_utc_now()

        if self.is_calculated:
            for amount_mod in self.values:
                sign = amount_mod['sign']
                unit = amount_mod['unit']
                amount_mod_func = TokenOperations.get_amount_modifier(sign, unit)
                result = amount_mod_func(result, amount_mod['amount'])

        if self.is_snapped:
            amount_mod_func = TokenOperations.get_snap_modifier(self.snap_to,
                                                                self.snap_unit)
            result = amount_mod_func(result)

        return result

    def __str__(self):
        res = NOW
        if self.is_calculated:
            res += ''.join(['{sign}{amount}{unit}'.format(**v)
                            for v in self.values])
        if self.is_snapped:
            res += '{}{}'.format(self.snap_to, self.snap_unit)
        return res
