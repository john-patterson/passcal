from pascal.AST import *
from pascal.Token import *
from pascal.Lexer import RESERVED_KEYWORDS


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_token = self._next()

    @staticmethod
    def error(msg=None):
        raise ParserError(msg)

    def _peek(self, n=0):
        if self.current + n >= len(self.tokens):
            return None
        return self.tokens[self.current + n]

    def _next(self):
        self.current += 1
        return self.tokens[self.current - 1]

    def _eat(self, type):
        if self.current_token is None:
            Parser.error('Eating on empty token.')
        elif self.current_token.type == type:
            self.current_token = self._next()
        else:
            Parser.error('Current token {} not of type {}.'.format(
                self.current_token,
                type
            ))

    def variable(self):
        node = Variable(self.current_token)
        self._eat(ID)
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self._eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def program(self):
        self._eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self._eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self._eat(DOT)
        return program_node

    def compound_statement(self):
        self._eat(BEGIN)
        nodes = self.statement_list()
        self._eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        node = self.statement()
        results = [node]

        while self.current_token.type == SEMI:
            self._eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error('Statements must be delimited by ;.')

        return results

    def statement(self):
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self._eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        node = Variable(self.current_token)
        self._eat(ID)
        return node

    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        decl = []
        if self.current_token.type == VAR:
            self._eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                decl.extend(var_decl)
                self._eat(SEMI)
        return decl

    def variable_declaration(self):
        var_nodes = [Variable(self.current_token)]
        self._eat(ID)

        while self.current_token.type == COMMA:
            self._eat(COMMA)
            var_nodes.append(Variable(self.current_token))
            self._eat(ID)

        self._eat(COLON)

        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]

        return var_declarations

    def type_spec(self):
        token = self.current_token
        if self.current_token.type == INTEGER:
            self._eat(INTEGER)
        elif self.current_token.type == REAL:
            self._eat(REAL)
        else:
            raise ParserError('{} not a type.'.format(token.type))
        node = Type(token)
        return node


    def empty(self):
        return NoOp()

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self._eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self._eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER_CONST:
            self._eat(INTEGER_CONST)
            return Number(token)
        elif token.type == REAL_CONST:
            self._eat(REAL_CONST)
            return Number(token)
        elif token.type == LPAREN:
            self._eat(LPAREN)
            node = self.expr()
            self._eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node
        self.error('Parse error, no factor.')

    def term(self):
        node = self.factor()

        while self.current_token.type in (STAR, FLOAT_DIV, INTEGER_DIV):
            token = self.current_token
            if token.type == STAR:
                self._eat(STAR)
            elif token.type == FLOAT_DIV:
                self._eat(FLOAT_DIV)
            elif token.type == INTEGER_DIV:
                self._eat(INTEGER_DIV)

            node = BinaryOperation(
                left=node,
                op=token,
                right=self.factor()
            )

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self._eat(PLUS)
            elif token.type == MINUS:
                self._eat(MINUS)

            node = BinaryOperation(
                left=node,
                op=token,
                right=self.term()
            )

        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node


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
    print(tokens)
    print('------------->')
    print(ast)

