import unittest

from pascal.Interpreter import Interpreter
from pascal.Parser import Parser
from tests.shared import make_tokens


class TestInterpreter(unittest.TestCase):
    def verify_arithmetic(self, evaluates_to, *args):
        token_stream = make_tokens(*args)

        # TODO: Remove dependency on parser
        #   Need a way to build parse trees in test methods.
        ast = Parser(token_stream).expr()
        result = Interpreter(ast).run()
        self.assertEqual(evaluates_to, result)

    def test_simple(self):
        self.verify_arithmetic(3, 1, '+', 2)
        self.verify_arithmetic(-1, 1, '-', 2)
        self.verify_arithmetic(2, 1, '*', 2)
        self.verify_arithmetic(0.5, 1, '/', 2)

    def test_precedence(self):
        self.verify_arithmetic(7, 1, '+', 2, '*', 3)
        self.verify_arithmetic(8, 10, '-', 4, '/', 2)

    def test_parens(self):
        self.verify_arithmetic(9, '(', 1, '+', 2, ')', '*', 3, ')')

    def test_fromtutorial(self):
        self.verify_arithmetic(3, 3)
        self.verify_arithmetic(30, 2, '+', 7, '*', 4)
        self.verify_arithmetic(5, 7, '-', 8, '/', 4)
        self.verify_arithmetic(17, 14, '+', 2, '*', 3, '-', 6, '/', 2)
        self.verify_arithmetic(22, 7, '+', 3, '*', '(', 10, '/', '(', 12, '/', '(', 3, '+', 1, ')', '-', 1, ')', ')')
        self.verify_arithmetic(10, 7, '+', 3, '*', '(', 10, '/', '(', 12, '/', '(', 3, '+', 1, ')', '-', 1, ')', ')', \
                               '/', '(', 2, '+', 3, ')', '-', 5, '-', 3, '+', '(', 8, ')')

