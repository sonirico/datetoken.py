try:
    # Python3.3 and above
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence


class InvalidTokenException(Exception):
    def __init__(self, token, errors=None):
        self.message = 'Token "{}" is invalid'.format(token)
        if errors and isinstance(errors, Sequence):
            self.message += ". {}".format(".".join(errors))
