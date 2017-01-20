import unittest

from tests.shared import make_tokens
from pascal.Lexer import Lexer
from pascal.Token import Token, \
    PLUS, MINUS, STAR, SLASH, EOF, INT, LPAREN, RPAREN


class TestLexer(unittest.TestCase):
    @staticmethod
    def tokenize(code):
        lexer = Lexer(code)
        return lexer.get_tokens()

    def verify(self, expr, *args):
        result = TestLexer.tokenize(expr)
        expected = make_tokens(*args)
        self.assertSequenceEqual(expected, result)

    def test_simple(self):
        for op in ['+', '-', '*', '/']:
            self.verify('1{}2'.format(op), 1, op, 2)

    def test_multidigit(self):
        for op in ['+', '-', '*', '/']:
            self.verify('11{}29'.format(op), 11, op, 29)

    def test_whitespace_invariant(self):
        for op in ['+', '-', '*', '/']:
            self.verify('11 \t {}   29'.format(op), 11, op, 29)

    def test_mixed_symbols(self):
        self.verify('1 + 2 * 3 / 4', 1, '+', 2, '*', 3, '/', 4)

    def test_parens(self):
        self.verify('1 + (2 * 3)', 1, '+', '(', 2, '*', 3, ')')

    def test_identifier(self):
        self.verify('test', 'TEST')
        self.verify('1+test', 1, '+', 'TEST')

    def test_assign_semi_dot(self):
        self.verify(':=', ':=')
        self.verify('test := 1 + 1', 'TEST', ':=', 1, '+', 1)
        self.verify('.:=test;', '.', ':=', 'TEST', ';')

    def test_case_insensitive(self):
        self.verify('beGin number := 2 ; a := NUMbEr; EnD;',
                    'BEGIN', 'NUMBER', ':=', 2, ';', 'A',
                    ':=', 'NUMBER', ';', 'END', ';')

    def test_integer_division(self):
        self.verify('div/', 'DIV', '/')

