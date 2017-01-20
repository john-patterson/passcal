from pascal.Parser import Parser
from pascal.Lexer import Lexer
from pascal.Token import Token, \
    INT, PLUS, MINUS, STAR, SLASH, LPAREN, RPAREN, EOF

GLOBAL_SCOPE = {}

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

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Variable(self, node):
        var_name = node.value
        val = GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def run(self):
        return self.visit(self.ast)


if __name__ == '__main__':
    sample = '''
    BEGIN
        BEGIN
            number := 2;
            a := number;
            b := 10 * a + 10 * number / 4;
            c := a - - b
        END;
        x := 11;
    END.
    '''
    from pascal.Lexer import Lexer
    tokens = Lexer(sample).get_tokens()
    ast = Parser(tokens).parse()
    Interpreter(ast).run()
    print(tokens)
    print('------------->')
    print(ast)
    print(GLOBAL_SCOPE)

