from pascal.AST import BinaryOperation, Number
from pascal.Token import Token,\
    ADD, SUB, MUL, DIV, INT, LPAREN, RPAREN, EOF


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_token = self._next()

    @staticmethod
    def error(msg=None):
        raise ParserError(msg)

    def _peek(self, n=0):
        if self.current + n >= len(self.tokens):
            return None
        return self.tokens[self.current + n]

    def _next(self):
        self.current += 1
        return self.tokens[self.current - 1]

    def _eat(self, type):
        if self.current_token is None:
            Parser.error('Eating on empty token.')
        elif self.current_token.type == type:
            self.current_token = self._next()
        else:
            Parser.error('Current token {} not of type {}.'.format(
                self.current_token,
                type
            ))

    def factor(self):
        token = self.current_token
        if token.type == INT:
            self._eat(INT)
            return Number(token)
        elif token.type == LPAREN:
            self._eat(LPAREN)
            node = self.expr()
            self._eat(RPAREN)
            return node
        self.error('Parse error, no factor.')

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self._eat(MUL)
            elif token.type == DIV:
                self._eat(DIV)

            node = BinaryOperation(
                left=node,
                op=token,
                right=self.factor()
            )

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (ADD, SUB):
            token = self.current_token
            if token.type == ADD:
                self._eat(ADD)
            elif token.type == SUB:
                self._eat(SUB)

            node = BinaryOperation(
                left=node,
                op=token,
                right=self.term()
            )

        return node

    def parse(self):
        return self.expr()
