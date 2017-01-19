ADD = 'ADD'
EOF = 'EOF'
INT = 'INT'


class Token:
    def __init__(self, type, text='', literal=None):
        self.type = type
        self.text = text
        self.literal = literal

    def __eq__(self, other):
        return self.type == other.type \
               and self.text == other.text \
               and self.literal == other.literal

    def __str__(self):
        return '<Token ({type}, {text})>'.format(
            type=self.type,
            text=self.text
        )

    def __repr__(self):
        return self.__str__()


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, code):
        self.code = code
        self.start = 0
        self.current = 0
        self.tokens = []

    @staticmethod
    def _error(msg):
        raise LexerError(msg)

    def _advance(self):
        self.current += 1
        return self.code[self.current - 1]

    def _eof(self):
        return self.current >= len(self.code)

    def _peek(self, n=0):
        if self.current + n >= len(self.code):
            return '\0'
        return self.code[self.current + n]

    def _current_lexeme(self):
        return self.code[self.start:self.current]

    def _add_token(self, type, payload=None):
        text = self._current_lexeme()
        self.tokens.append(Token(type, text, payload))

    def _number(self):
        while self._peek().isdigit():
            self._advance()
        text = self._current_lexeme()
        self._add_token(INT, int(text))

    def _whitespace(self):
        while self._peek().isspace():
            self._advance()

    def _scan_token(self):
        c = self._advance()
        if c == '+':
            self._add_token(ADD)
        else:
            if c.isdigit():
                self._number()
            else:
                Lexer._error('Could not classify {}.'.format(
                    self._current_lexeme()
                ))

    def get_tokens(self):
        if len(self.tokens) > 0:
            return self.tokens
        while not self._eof():
            self._whitespace()
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(EOF))
        return self.tokens


class Interpreter:
    pass


if __name__ == '__main__':
    lexer = Lexer('1+2')
    print(lexer.get_tokens())
