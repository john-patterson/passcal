class AST:
    pass


class BinaryOperation(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __eq__(self, other):
        return isinstance(other, BinaryOperation) \
               and self.left == other.left \
               and self.token == other.token \
               and self.right == other.right

    def __str__(self):
        return '<BinOp ({}, {}, {})>'.format(
            repr(self.left),
            repr(self.token),
            repr(self.right)
        )

    __repr__ = __str__


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __eq__(self, other):
        return isinstance(other, UnaryOp) \
               and self.token == other.token \
               and self.expr == other.expr

    def __str__(self):
        return '<UnaryOp {}>'.format(self.token)

    __repr__ = __str__


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.literal

    def __eq__(self, other):
        return isinstance(other, Number) \
               and self.token == other.token \
               and self.value == other.value

    def __str__(self):
        return '<Number {}>'.format(self.value)

    __repr__ = __str__
