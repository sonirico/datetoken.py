from .models import SimpleToken
from .models import ComplexToken
from .parser import token_to_dict


class TokenFactory(object):
    @classmethod
    def from_string(cls, token):
        token_dict = token_to_dict(token)
        return cls.from_dict(token_dict)

    @staticmethod
    def from_dict(token):
        return ComplexToken(**token)


class SimpleTokenFactory(TokenFactory):
    @staticmethod
    def from_dict(token):
        amount, sign, unit = None, None, None

        token_values = token['values']
        if token_values:
            token_values = token_values[0]
            amount = token_values['amount']
            sign = token_values['sign']
            unit = token_values['unit']

        return SimpleToken(amount, unit, sign, **token)


class ComplexTokenFactory(TokenFactory):
    pass
