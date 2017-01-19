from pascal.Token import Token, \
    INT, ADD, SUB, MUL, DIV, LPAREN, RPAREN, EOF


class InterpreterError(Exception):
    pass


class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_token = self._next()

    @staticmethod
    def error(msg=None):
        raise InterpreterError(msg)

    def _peek(self, n=0):
        if self.current + n >= len(self.tokens):
            return None
        return self.tokens[self.current + n]

    def _next(self):
        self.current += 1
        return self.tokens[self.current - 1]

    def _eat(self, type):
        if self.current_token is None:
            Interpreter.error('Eating on empty token.')
        elif self.current_token.type == type:
            self.current_token = self._next()
        else:
            Interpreter.error('Current token {} not of type {}.'.format(
                self.current_token,
                type
            ))

    def factor(self):
        token = self.current_token
        if token.type == INT:
            self._eat(INT)
            return token.literal
        elif token.type == LPAREN:
            self._eat(LPAREN)
            result = self.expr()
            self._eat(RPAREN)
            return result
        self.error('Parse error, no factor.')

    def term(self):
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self._eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self._eat(DIV)
                result /= self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (ADD, SUB):
            token = self.current_token
            if token.type == ADD:
                self._eat(ADD)
                result += self.term()
            elif token.type == SUB:
                self._eat(SUB)
                result -= self.term()

        return result


if __name__ == '__main__':
    from pascal.Lexer import Lexer

    while True:
        try:
            text = input('> ')
        except KeyboardInterrupt:
            break
        if not text:
            continue
        if text == ':q':
            break
        print(Interpreter(Lexer(text).get_tokens()).expr())

