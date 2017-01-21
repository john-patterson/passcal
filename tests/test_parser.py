from unittest import TestCase
from pascal.AST import AST, BinaryOperation, UnaryOp, Number
from pascal.Token import *
from pascal.Parser import Parser
from pascal.Lexer import RESERVED_KEYWORDS

tokens = {
    '+': Token(PLUS, '+'),
    '-': Token(MINUS, '-'),
    '*': Token(STAR, '*'),
    '(': Token(LPAREN, '('),
    ')': Token(RPAREN, ')'),
    1: Token(INTEGER_CONST, '1', 1),
    EOF: Token(EOF),
}
tokens.update(RESERVED_KEYWORDS)


def parse(*stream, method='parse'):
    stream = [tokens[t] for t in stream]
    parser = Parser(stream)

    m = getattr(parser, method)
    if m is not None:
        return m()
    return None


class TestParser(TestCase):
    def test_number(self):
        tree = Number(tokens[1])
        ast = parse(1, EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_unary_plus(self):
        tree = UnaryOp(tokens['+'], Number(tokens[1]))
        ast = parse('+', 1, EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_unary_minus(self):
        tree = UnaryOp(tokens['+'], Number(tokens[1]))
        ast = parse('+', 1, EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_unary_plus_minus_minus(self):
        tree = UnaryOp(tokens['+'], UnaryOp(tokens['-'], UnaryOp(tokens['-'], Number(tokens[1]))))
        ast = parse('+', '-', '-', 1, EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_binary(self):
        tree = BinaryOperation(Number(tokens[1]), tokens['+'], Number(tokens[1]))
        ast = parse(1, '+', 1, EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_nested_binary(self):
        tree = BinaryOperation(BinaryOperation(Number(tokens[1]), tokens['+'], Number(tokens[1])),
                               tokens['+'], Number(tokens[1]))
        ast = parse(1, '+', 1, '+', 1, EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_nested_binary_mixed_op(self):
        tree = BinaryOperation(BinaryOperation(Number(tokens[1]), tokens['*'], Number(tokens[1])),
                               tokens['+'], Number(tokens[1]))
        ast = parse(1, '*', 1, '+', 1, EOF, method='expr')
        self.assertEqual(tree, ast)
        tree = BinaryOperation(Number(tokens[1]), tokens['+'],
                               BinaryOperation(Number(tokens[1]), tokens['*'], Number(tokens[1])))
        ast = parse(1, '+', 1, '*', 1, EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_parens_break_precedence(self):
        tree = BinaryOperation(Number(tokens[1]), tokens['*'],
                               BinaryOperation(Number(tokens[1]), tokens['+'], Number(tokens[1])))
        ast = parse(1, '*', '(', 1, '+', 1, ')', EOF, method='expr')
        self.assertEqual(tree, ast)

    def test_integer_division(self):
        tree = BinaryOperation(Number(tokens[1]), RESERVED_KEYWORDS[DIV], Number(tokens[1]))
        ast = parse(1, 'DIV', 1, EOF, method='expr')
        self.assertEqual(tree, ast)
