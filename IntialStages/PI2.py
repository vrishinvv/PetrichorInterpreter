###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################


# Token types
INTEGER            =   'INTEGER'
PLUS               =   'PLUS'
MINUS              =   'MINUS'
MULT               =   'MULT'
DIV                =   'DIV'
EOF                =   'EOF'
LPAREN             =   '('
RPAREN             =   ')'

LESS_THAN          =   'LESS_THAN'
LESS_THAN_EQUAL    =   'LESS_THAN_EQUAL'
EQUALS             =   'EQUALS'
GREATER_THAN       =   'GREATER_THAN'
GREATER_THAN_EQUAL =   'GREATER_THAN_EQUAL'

BEGIN              =   '{'
END                =   '}'
IF                 =   'IF'
FI                 =   'FI'
THEN               =   'THEN'
ELSE               =   'ELSE'
ELSEIF             =   'ELSEIF'
FOO                =   'FOO'

SEMI               =   'SEMI'
DOT                =   'DOT'
ASSIGN             =   'ASSIGN'
ID                 =   'ID'



def is_operator(c):
    return c in ['+','-','*','/','<','>']

def recognise_operator(c):
    switcher ={
        '+':  PLUS,
        '-':  MINUS,
        '*':  MULT,
        '/':  DIV,
        '<':  LESS_THAN,
        '>':  GREATER_THAN
    }
    return switcher.get(c,'-1');


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=str(self.value)
        )

RESERVED_KEYWORDS = {
    'BEGIN': Token('BEGIN', '{'),
    'END': Token('END', '}'),
    'IF': Token('IF', 'IF'),
    'FI': Token('FI', 'FI'),
    'ELSE': Token('ELSE', 'ELSE'),
    'ELSEIF': Token('ELSEIF', 'ELSEIF'),

}

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token


    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self.current_char is not None:

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '{':
                self.advance()
                return Token(BEGIN, '{')

            if self.current_char == '}':
                self.advance()
                return Token(END, '}')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(LESS_THAN_EQUAL, '<=')

            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(GREATER_THAN_EQUAL, '>=')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(EQUALS, '==')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if is_operator(self.current_char):
                t = Token(recognise_operator(self.current_char),self.current_char)
                self.advance()
                return t

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')


            self.error()

        return Token(EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = op
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        #expr is an AST node here, remeber it has to be one so that visit_
        self.token = op
        self.op = op
        self.expr = expr

# Compound AST node represents a compound statement. 
# It contains a list of statement nodes in its children variable.
class Compound(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class IfBlock(AST):
    def __init__(self, cond, token, if_body, elseif_nodes,else_body):
        self.cond = cond
        self.token = token
        self.if_body = if_body
        self.elseif_nodes = elseif_nodes
        self.else_body = else_body

class ElseIfBlock(AST):
    def __init__(self, cond, token, body):
        self.cond = cond
        self.token = token
        self.body = body

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Error parsing input')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN"""

        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif(token.type==INTEGER):
            self.eat(INTEGER)
            return Num(token)
        elif(token.type==LPAREN):
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable();
            return node

    def term(self):
        """term: factor ((MUL | DIV | LESS_THAN | LESS_THAN_EQUAL | EQUALS | GREATER_THAN | GREATER_THAN_EQUAL) factor)*"""
        node = self.factor()

        while self.current_token.type in (MULT, DIV, LESS_THAN, LESS_THAN_EQUAL, EQUALS, GREATER_THAN, GREATER_THAN_EQUAL):
            token = self.current_token

            if token.type == MULT:
                self.eat(MULT)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == LESS_THAN:
                self.eat(LESS_THAN)
            elif token.type == LESS_THAN_EQUAL:
                self.eat(LESS_THAN_EQUAL)
            elif token.type == EQUALS:
                self.eat(EQUALS)
            elif token.type == GREATER_THAN:   
                self.eat(GREATER_THAN)
            elif token.type == GREATER_THAN_EQUAL:
                self.eat(GREATER_THAN_EQUAL)

            node = BinOp(left=node, op=token, right=self.factor()); 

        return node

    def expr(self):
        """expr   : term ((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term());
        
        return node


    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        print(3, self.current_token)
        self.eat(BEGIN)
        print(4, self.current_token)
        nodes = self.statement_list()
        print(5, self.current_token)
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | if_block
                  | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == IF:
            node = self.if_block()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def elseif_block(self):
        """ 
        elseif_block: ELSEIF expr compound_statement 
        """
        token = self.current_token
        self.eat(ELSEIF)
        cond = self.expr()
        body = self.compound_statement()
        
        node= ElseIfBlock(cond, token, body)
        return node

    def if_block(self):
        """ 
        if_block: IF expr 
                    compound_statement 
                | (ELSEIF
                    compound_statement)*
                | ELSE
                    compount_statement
                | empty
                  FI
        """
        token = self.current_token
        self.eat(IF)
        cond = self.expr();
        if_body = self.compound_statement()
        elseif_nodes=[]
        while (self.current_token.type == ELSEIF):
            print(1)
            elseif_nodes.append(self.elseif_block())

        if(self.current_token.type == ELSE):
            self.eat(ELSE)
            else_body = self.compound_statement()
        else:
            else_body = self.empty()

        self.eat(FI)
        print(len(elseif_nodes))
        node= IfBlock(cond, token, if_body, elseif_nodes, else_body)
        return node

    def empty(self):
        """
        An empty production
        """
        return NoOp()

    def program(self):
        """
        program : compound_statement DOT
        """

        node = self.compound_statement()
        self.eat(DOT)
        return node

    def parse(self):
        """ 
        program : compound_statement DOT

        compound_statement : BEGIN statement_list END

        statement_list : statement
                       | statement SEMI statement_list

        statement : compound_statement
                  | assignment_statement
                  | if_block
                  | empty

        assignment_statement : variable ASSIGN expr
    
        empty :
        
       
        if_block: IF expr 
                    compound_statement 
                | elseif_block
                | ELSE
                    compount_statement
                | empty
                  FI
    
        elseif_block: ELSEIF expr 
                        compound_statement 

        expr: term ((PLUS | MINUS) term)*

        term: factor ((MUL | DIV | LESS_THAN | LESS_THAN_EQUAL | EQUALS | GREATER_THAN | GREATER_THAN_EQUAL) factor)*

        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LPAREN expr RPAREN
               | variable

    
        variable: ID 
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    GLOBAL_SCOPE={}
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MULT:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == LESS_THAN:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == LESS_THAN_EQUAL:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == EQUALS:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == GREATER_THAN:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == GREATER_THAN_EQUAL:
            return self.visit(node.left) >= self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        #stroing it in symbol table
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
    
    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_IfBlock(self, node):
        if self.visit(node.cond):
            self.visit(node.if_body)
            return

        print('here', len(node.elseif_nodes))
        for n in node.elseif_nodes:
            print('here_again')
            ok = self.visit(n)
            if ok:
                return
        
        self.visit(node.else_body)

    def visit_ElseIfBlock(self, node):
        print(node.cond)
        if self.visit(node.cond):
            self.visit(node.body)
            return 1

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while True:
        # try:
        #     try:
        #         text = raw_input('spi> ')
        #     except NameError:  # Python3
        #         text = input('spi> ')
        # except EOFError:
        #     break
        # if not text:
        #     continue
        text = """\
                {
                
                    {
                        number = 2;
                        a = --1;
                        IF (a<1) { 
                            hello=5  
                        }
                        ELSEIF (a<2) {
                            hello=6 
                        }
                        ELSEIF (a<3) {
                            hello=7  
                        }
                        ELSEIF (a<4) { 
                            hello=8  
                        }
                        ELSEIF (a<5) {
                            hello=9  
                        }
                        ELSEIF (a<6) {
                            hello=10 
                        }
                        ELSEIF (a<7) {
                            hello=11 
                        }
                        ELSE { 
                            hello=12 
                        }
                        FI;

                        b = a < a+ 10 * number >= 4;
                        c = a - - b
                    };
                
                    x = 11;
                }.
                 """

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
        print(interpreter.GLOBAL_SCOPE.get('hello'))
        break


if __name__ == '__main__':
    main()
