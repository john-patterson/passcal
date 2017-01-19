from pascal.Token import Token, \
    INT, ADD, SUB, MUL, DIV, LPAREN, RPAREN, EOF


def make_tokens(*args):
    def make_token(a):
        if isinstance(a, int):
            return Token(INT, str(a), a)
        elif a == '+':
            return Token(ADD, '+')
        elif a == '-':
            return Token(SUB, '-')
        elif a == '*':
            return Token(MUL, '*')
        elif a == '/':
            return Token(DIV, '/')
        elif a == '(':
            return Token(LPAREN, '(')
        elif a == ')':
            return Token(RPAREN, ')')

    token_stream = [make_token(a) for a in args]
    token_stream.append(Token(EOF))
    return token_stream
