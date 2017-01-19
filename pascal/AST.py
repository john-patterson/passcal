class AST:
    pass


class BinaryOperation(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return '<BinOp ({}, {}, {})>'.format(
            repr(self.left),
            repr(self.token),
            repr(self.right)
        )

    def __repr__(self):
        return self.__str__()


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.literal

    def __str__(self):
        return '<Number {}>'.format(self.value)

    def __repr__(self):
        return self.__str__()

