import unittest
from .context import pascal
from pascal.Lexer import Lexer, Token, INT, ADD, EOF


class LexerTest(unittest.TestCase):
    @staticmethod
    def tokenize(code):
        lexer = Lexer(code)
        return lexer.get_tokens()

    def test_simpleaddition(self):
        result = LexerTest.tokenize('1+2')
        expected = [
            Token(INT, '1', 1),
            Token(ADD, '+'),
            Token(INT, '2', 2),
            Token(EOF)
        ]
        self.assertSequenceEqual(expected, result)

    def test_addition_multidigit(self):
        result = LexerTest.tokenize('11+29')
        expected = [
            Token(INT, '11', 11),
            Token(ADD, '+'),
            Token(INT, '29', 29),
            Token(EOF)
        ]
        self.assertSequenceEqual(expected, result)

    def test_addition_whitespace_invariant(self):
        result = LexerTest.tokenize('11 \t +  29')
        expected = [
            Token(INT, '11', 11),
            Token(ADD, '+'),
            Token(INT, '29', 29),
            Token(EOF)
        ]
        self.assertSequenceEqual(expected, result)
