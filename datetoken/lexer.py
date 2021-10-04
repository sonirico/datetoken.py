from .token import Token, TokenType


class Lexer(object):
    def __init__(self, raw_token=""):
        self.input = raw_token.strip()
        self.position = 0
        self.read_position = 0
        self.current_char = ""

        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.current_char = ""
        else:
            self.current_char = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self):
        if self.read_position >= len(self.input):
            return None
        return self.input[self.read_position]

    def next_token(self):
        if "+" == self.current_char:
            tok = Token(TokenType.PLUS, self.current_char)
        elif "-" == self.current_char:
            tok = Token(TokenType.MINUS, self.current_char)
        elif "/" == self.current_char:
            tok = Token(TokenType.SLASH, self.current_char)
        elif "@" == self.current_char:
            tok = Token(TokenType.AT, self.current_char)
        elif "n" == self.current_char:
            if "o" != self.peek_char():
                return Token(TokenType.ILLEGAL, self.current_char)
            self.read_char()
            if "w" != self.peek_char():
                return Token(TokenType.ILLEGAL, self.current_char)
            self.read_char()
            tok = Token(TokenType.NOW, "now")
        elif self.current_char.isdigit():
            return Token(TokenType.NUMBER, self.read_number())
        elif self.current_char == "":
            tok = Token(TokenType.END, "")
        elif self.current_char.isalpha():
            return Token(TokenType.MODIFIER, self.read_word())
        else:
            tok = Token(TokenType.ILLEGAL, self.current_char)
        self.read_char()
        return tok

    def read_word(self):
        pos = self.position
        while self.current_char.isalpha() or self.current_char.isdigit():
            self.read_char()
        return self.input[pos : self.position]

    def read_number(self):
        pos = self.position
        while self.current_char.isdigit():
            self.read_char()
        return self.input[pos : self.position]
