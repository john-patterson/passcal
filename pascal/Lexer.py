from pascal.Token import *


RESERVED_KEYWORDS = {
    BEGIN: Token(BEGIN, BEGIN),
    END: Token(END, END),
    DIV: Token(INTEGER_DIV, DIV),
    PROGRAM: Token(PROGRAM, PROGRAM),
    VAR: Token(VAR, VAR),
    INTEGER: Token(INTEGER, INTEGER),
    REAL: Token(REAL, REAL)
}


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

    def _id(self):
        while self._peek().isalnum():
            self._advance()
        text = self._current_lexeme().upper()
        token = RESERVED_KEYWORDS.get(text, Token(ID, text))
        self.tokens.append(token)

    def _number(self):
        while self._peek().isdigit():
            self._advance()
        if self._peek() == '.':
            self._advance()
            while self._peek().isdigit():
                self._advance()
            text = self._current_lexeme()
            self._add_token(REAL_CONST, float(text))
        else:
            text = self._current_lexeme()
            self._add_token(INTEGER_CONST, int(text))


    def _whitespace(self):
        while self._peek().isspace():
            self._advance()

    def _comment(self):
        while self._peek() != '}':
            self._advance()
        self._advance()

    def _scan_token(self):
        c = self._advance()
        if c == '+':
            self._add_token(PLUS)
        elif c == '{':
            self._comment()
        elif c == ',':
            self._add_token(COMMA)
        elif c == '-':
            self._add_token(MINUS)
        elif c == '*':
            self._add_token(STAR)
        elif c == '/':
            self._add_token(FLOAT_DIV)
        elif c == '(':
            self._add_token(LPAREN)
        elif c == ')':
            self._add_token(RPAREN)
        elif c == ':' and self._peek() == '=':
            self._advance()
            self._add_token(ASSIGN)
        elif c == ':':
            self._add_token(COLON)
        elif c == ';':
            self._add_token(SEMI)
        elif c == '.':
            self._add_token(DOT)
        elif c == '_':
            e = LexerError('_ is not a valid identifier')
            try:
                n = self._advance()
                if not n.isalnum():
                    raise e
                self._id()
            except IndexError:
                raise e
        elif c.isalpha():
            self._id()
        elif c.isdigit():
            self._number()
        else:
            Lexer._error('Could not classify {}.'.format(
                self._current_lexeme()
            ))

    def get_tokens(self):
        if len(self.tokens) > 0:
            return self.tokens
        self._whitespace()
        while not self._eof():
            self.start = self.current
            self._scan_token()
            self._whitespace()
        self.tokens.append(Token(EOF))
        return self.tokens

if __name__ == '__main__':
    sample = open('../sample/part10.pas', 'r').read()
    lexer = Lexer(sample)
    print(lexer.get_tokens())
