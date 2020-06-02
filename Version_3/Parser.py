from Lexer import *


""" 
    GRAMMAR:
        program: FUNC*
        func : FUNC ID (param) compound_statement
        
        param: empty|(var|expr)*
        
        compound_statement: BEGIN statement_list END
        
        statement_list : (assignment_statement | empty| if_block| print | for_block | call)*
        
        assignment_statement : variable ASSIGN expr SEMI
        
        empty :
        
        print : PRINT( ((str|expr)COMMA)*  )  
        
        call : CALL ID (param) SEMI

        if_block: IF expr 
                    compound_statement
                | elseif_block
                | ELSE
                    compount_statement
                | empty

    
        elseif_block: ELSEIF expr 
                        compound_statement 
    
        for_block: FOR(assignment_statement; cond; change) 
            compounf_statement

        expr: term ((PLUS | MINUS) term)*

        term: factor ((MUL | DIV | LESS_THAN | LESS_THAN_EQUAL | EQUALS | GREATER_THAN | GREATER_THAN_EQUAL) factor)*

        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LPAREN expr RPAREN
               | variable

    
        variable: ID 
"""

class AST(object):
    pass

class Func(AST):
    def __init__(self, token, name, var_param, body):
        self.token = token
        self.name = name.value
        self.body= body
        self.var_param=var_param
        self.val_param=[]

class Param(AST):
    def __init__(self, token, val_param):
        self.token = token
        self.val_param=val_param

class Call(AST):
    def __init__(self, token, val_param, name):
        self.token = token
        self.name = name.value
        self.val_param = val_param

class Return(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value

class Print(AST):
    def __init__(self, token, content):
        self.token = token
        self.content = content 

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

class Compound(AST):
    # Compound AST node represents a compound statement. 
    # It contains a list of statement nodes in its children variable.
    #Represents a 'BEGIN ... END' block
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

class ForBlock(AST):
    def __init__(self, token, assign, cond, change, body):
        self.token = token
        self.assign = assign
        self.cond = cond
        self.change = change
        self.body = body

class IfBlock(AST):
    def __init__(self, cond, token, if_body, elseif_nodes, else_body):
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

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, expected, recieved):
        
        self.lexer.err.res.append(' Invalid Syntax Error -- COMPILE TIME ERROR'
                        +'\n      Expected: '+expected
                        +'\n      Recieved: '+recieved
                        +'\n      At line:  '+str(self.lexer.line)
                        +'\n      Wrong char:  '+str(self.current_token.value)
                        )
        
        

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type,self.current_token.type)
            #self.current_token = self.lexer.get_next_token()
            self.eat(self.current_token.type)
            return

    def param(self, expected):
        """
        param: empty|(expr COMMA)*
        """
        # to tell me, if the param list is only variables, or only values
        # if function recieved paramter 1 - then im execting strictly variables,
        # else I am expecting expressions
        ok1 = ok2 = 0;
        token=self.current_token
        #node = self.empty();

        result = [];
        while(self.current_token.type in (ID, PLUS, MINUS, LPAREN, INTEGER, CALL)):
            if(expected == 1):
                node = self.variable()
                ok1=1
            elif(expected==2):
                node = self.expr()
                ok2=1
            result.append(node)
            self.eat(COMMA)

        if(ok1+ok2 == 2):
            raise Exception('You have mix matched the paramter types allowed')
        elif(ok1+ok2==0):
            return result
        else:
            if(expected==1 and ok1==1):
                return result
            elif(expected==2 and ok2==1):
                return result
            else:
                raise Exception('Parameter type does not match what the code expects')

    def func(self):
        """
        func : FUNC ID (param) compound_statement  
        """
        token=self.current_token
        self.eat(FUNC)
        name = self.variable()
        self.eat(LPAREN)
        var_param = self.param(1)
        self.eat(RPAREN)
        body = self.compound_statement()


        return Func(token, name, var_param, body)

    def call(self):
        """
        call : CALL ID (param)
        """
        token=self.current_token
        self.eat(CALL)
        name = self.variable()
        self.eat(LPAREN)
        val_param = self.param(2)
        self.eat(RPAREN)

        return Call(token, val_param, name)

    def print(self):
        """ 
        PRINT( ((str|expr)COMMA)*  ) 
        """
        token = self.current_token
        node = self.empty()
        result = [node]
        self.eat(PRINT)
        self.eat(LPAREN)
        while(self.current_token.type in (STR, ID, PLUS, MINUS,INTEGER, LPAREN, CALL)):
            if(self.current_token.type == STR):
                node = self.current_token.value
                self.eat(STR)
            elif(self.current_token.type in (ID, PLUS, MINUS,INTEGER, LPAREN, CALL)):
                node = self.expr()

            result.append(node)
            self.eat(COMMA)

        self.eat(RPAREN)
        

        return Print(token, result)

    def ret(self):
        """
        RETURN exp|empty 
        """
        token=self.current_token
        self.eat(RETURN)
        if(self.current_token.type in (ID,PLUS,MINUS,INTEGER,LPAREN,CALL)):
            node = self.expr()
            return Return(token,node)

        
        node = NoOp()
        return Return(token,node)

    def factor(self):
        """
        factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN | call

        """
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
        elif(token.type==CALL):
            node = self.call()
            return node
        else:
            node = self.variable();
            return node

    def term(self):
        """
        term: factor ((MUL | DIV | LESS_THAN | LESS_THAN_EQUAL | EQUALS | GREATER_THAN | GREATER_THAN_EQUAL) factor)*
        """
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
        """
        expr   : term ((PLUS | MINUS) term)*
        """
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
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : (assignment_statement | empty| if_block| print | for_block|expr|return )*
        """
        node=self.empty()
        result=[node]
        while(self.current_token.type in (ID, IF, PRINT, FOR, CALL, RETURN)):
            if self.current_token.type == ID:
                node = self.assignment_statement()
                self.eat(SEMI)
            elif self.current_token.type == IF:
                node = self.if_block()

            elif self.current_token.type == FOR:
                node = self.for_block()    

            elif self.current_token.type == PRINT:
                node = self.print()
                self.eat(SEMI)
            elif self.current_token.type == CALL:
                node = self.call()
                self.eat(SEMI)
            elif self.current_token.type == RETURN:
                node = self.ret()
                self.eat(SEMI)
                
            result.append(node)
        
        return result

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
        """
        token = self.current_token
        self.eat(IF)
        cond = self.expr();
        if_body = self.compound_statement()
        elseif_nodes=[]
        while (self.current_token.type == ELSEIF):
            elseif_nodes.append(self.elseif_block())

        if(self.current_token.type == ELSE):
            self.eat(ELSE)
            else_body = self.compound_statement()
        else:
            else_body = self.empty()

        node= IfBlock(cond, token, if_body, elseif_nodes, else_body)
        return node

    def for_block(self):
        """
            for_block: FOR(assignment_statement COMMA cond COMMA change COMMA) 
                            compounf_statement
        """
        token = self.current_token
        self.eat(FOR)
        self.eat(LPAREN)
        assig = self.assignment_statement()
        self.eat(COMMA)
        cond = self.expr()
        self.eat(COMMA)
        change = self.assignment_statement()
        self.eat(COMMA)
        self.eat(RPAREN)
        body = self.compound_statement()
        return ForBlock(token,assig,cond,change,body)

    def empty(self):
        """
        An empty production
        """
        return NoOp()

    def program(self):
        """
        program: FUNC*
        """
        result = []
        while self.current_token.type == FUNC:
            node=self.func()
            result.append(node)

        return result

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error(EOF,self.current_token.type)

        return node