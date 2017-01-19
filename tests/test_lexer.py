import unittest

from tests.shared import make_tokens
from pascal.Lexer import Lexer
from pascal.Token import Token, \
    ADD, SUB, MUL, DIV, EOF, INT, LPAREN, RPAREN


class TestLexer(unittest.TestCase):
    @staticmethod
    def tokenize(code):
        lexer = Lexer(code)
        return lexer.get_tokens()

    def verify_arithmetic(self, expr, *args):
        result = TestLexer.tokenize(expr)
        expected = make_tokens(*args)
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
