
class InvalidTokenException(Exception):
    def __init__(self, token):
        self.message = 'Token "{}" is invalid'.format(token)
