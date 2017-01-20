from pascal.Token import Token, \
    INT, PLUS, MINUS, STAR, SLASH, LPAREN, RPAREN, EOF, ID, \
    ASSIGN, SEMI, DOT


def make_tokens(*args):
    def make_token(a):
        if isinstance(a, int):
            return Token(INT, str(a), a)
        elif a == '+':
            return Token(PLUS, '+')
        elif a == '-':
            return Token(MINUS, '-')
        elif a == '*':
            return Token(STAR, '*')
        elif a == '/':
            return Token(SLASH, '/')
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
        else:
            return Token(ID, a)

    token_stream = [make_token(a) for a in args]
    token_stream.append(Token(EOF))
    return token_stream
