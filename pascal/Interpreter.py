from pascal.Parser import Parser
from pascal.Lexer import Lexer
from pascal.Token import Token, \
    INT, PLUS, MINUS, STAR, SLASH, LPAREN, RPAREN, EOF


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


class ReversePolishTranslator(NodeVisitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_BinaryOperation(self, node):
        op = node.op.text
        return '{} {} {}'.format(
            self.visit(node.left),
            self.visit(node.right),
            op
        )

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Number(self, node):
        return node.value


class LispTranslator(NodeVisitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_BinaryOperation(self, node):
        op = node.op.text
        return '({} {} {})'.format(
            op,
            self.visit(node.left),
            self.visit(node.right),
        )

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Number(self, node):
        return node.value


class Interpreter(NodeVisitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_BinaryOperation(self, node):
        t = node.op.type
        if t == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif t == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif t == STAR:
            return self.visit(node.left) * self.visit(node.right)
        elif t == SLASH:
            return self.visit(node.left) / self.visit(node.right)

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Number(self, node):
        return node.value

    def run(self):
        return self.visit(self.ast)


if __name__ == '__main__':
    lexer = Lexer('5---2')
    tokens = lexer.get_tokens()
    ast = Parser(tokens).parse()
    print(Interpreter(ast).run())
    print(ReversePolishTranslator(ast).visit(ast))
    print(LispTranslator(ast).visit(ast))
