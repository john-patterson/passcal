class Token:
    def __init__(self, type, text='', literal=None):
        self.type = type
        self.text = text
        self.literal = literal

    def __eq__(self, other):
        return isinstance(other, Token) \
               and self.type == other.type \
               and self.text == other.text \
               and self.literal == other.literal

    def __str__(self):
        return '<Token ({type}, {text})>'.format(
            type=self.type,
            text=self.text
        )

    def __repr__(self):
        return self.__str__()


PLUS = 'PLUS'
MINUS = 'MINUS'
STAR = 'STAR'
SLASH = 'SLASH'
EOF = 'EOF'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
ASSIGN = 'ASSIGN'
SEMI = 'SEMI'
DOT = 'DOT'
BEGIN = 'BEGIN'
END = 'END'
DIV = 'DIV'
VAR = 'VAR'
PROGRAM = 'PROGRAM'
INTEGER = 'INTEGER'
REAL = 'REAL'
COMMA = 'COMMA'
COLON = 'COLON'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
