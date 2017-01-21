from pascal.Token import *
from pascal.Lexer import RESERVED_KEYWORDS


def make_tokens(*args):
    def make_token(a):
        if isinstance(a, int):
            return Token(INTEGER_CONST, str(a), a)
        elif a == '+':
            return Token(PLUS, '+')
        elif a == '-':
            return Token(MINUS, '-')
        elif a == '*':
            return Token(STAR, '*')
        elif a == '/':
            return Token(FLOAT_DIV, '/')
        elif a == '(':
            return Token(LPAREN, '(')
        elif a == ')':
            return Token(RPAREN, ')')
        elif a == ':=':
            return Token(ASSIGN, ':=')
        elif a == '.':
            return Token(DOT, '.')
        elif a == ';':
            return Token(SEMI, ';')
        elif a.upper() in RESERVED_KEYWORDS.keys():
            return RESERVED_KEYWORDS[a.upper()]
        else:
            return Token(ID, a)

    token_stream = [make_token(a) for a in args]
    token_stream.append(Token(EOF))
    return token_stream
