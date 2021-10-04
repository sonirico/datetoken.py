class TokenType(object):
    END = ""
    ILLEGAL = "ILLEGAL"
    # Operators
    PLUS = "+"
    MINUS = "-"
    SLASH = "/"
    AT = "@"
    # Identifiers
    NUMBER = "NUMBER"
    MODIFIER = "MODIFIER"
    # keywords
    NOW = "NOW"


class Token(object):
    def __init__(self, tok_type, tok_literal):
        self.token_type = tok_type
        self.token_literal = tok_literal
