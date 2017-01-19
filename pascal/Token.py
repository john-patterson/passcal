class Token:
    def __init__(self, type, text='', literal=None):
        self.type = type
        self.text = text
        self.literal = literal

    def __eq__(self, other):
        return self.type == other.type \
               and self.text == other.text \
               and self.literal == other.literal

    def __str__(self):
        return '<Token ({type}, {text})>'.format(
            type=self.type,
            text=self.text
        )

    def __repr__(self):
        return self.__str__()


ADD = 'ADD'
SUB = 'SUB'
MUL = 'MUL'
DIV = 'DIV'
EOF = 'EOF'
INT = 'INT'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'