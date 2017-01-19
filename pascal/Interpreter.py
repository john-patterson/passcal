from pascal.Parser import Parser
from pascal.Lexer import Lexer
from pascal.Token import Token, \
    INT, ADD, SUB, MUL, DIV, LPAREN, RPAREN, EOF


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(
            type(node).__name__
        ))

class InterpreterError(Exception):
    pass


class Interpreter(NodeVisitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_BinaryOperation(self, node):
        t = node.op.type
        if t == ADD:
            return self.visit(node.left) + self.visit(node.right)
        elif t == SUB:
            return self.visit(node.left) - self.visit(node.right)
        elif t == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif t == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
        return node.value

    def run(self):
        return self.visit(self.ast)
