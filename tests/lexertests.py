import unittest

from pascal.Lexer import Lexer, Token, \
    INT, ADD, SUB, MUL, DIV, EOF, LPAREN, RPAREN


class LexerTest(unittest.TestCase):
    @staticmethod
    def tokenize(code):
        lexer = Lexer(code)
        return lexer.get_tokens()

    def verify_arithmetic(self, expr, *args):
        result = LexerTest.tokenize(expr)

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

        expected = [make_token(a) for a in args]
        expected.append(Token(EOF))
        self.assertSequenceEqual(expected, result)

    def test_simple(self):
        for op in ['+', '-', '*', '/']:
            self.verify_arithmetic('1{}2'.format(op), 1, op, 2)

    def test_multidigit(self):
        for op in ['+', '-', '*', '/']:
            self.verify_arithmetic('11{}29'.format(op), 11, op, 29)

    def test_whitespace_invariant(self):
        for op in ['+', '-', '*', '/']:
            self.verify_arithmetic('11 \t {}   29'.format(op), 11, op, 29)

    def test_mixed_symbols(self):
        self.verify_arithmetic('1 + 2 * 3 / 4', 1, '+', 2, '*', 3, '/', 4)

    def test_parens(self):
        self.verify_arithmetic('1 + (2 * 3)', 1, '+', '(', 2, '*', 3, ')')
