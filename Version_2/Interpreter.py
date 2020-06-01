
###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################
from Parser import *


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    GLOBAL_SCOPE={}
    GLOBAL_FUNC_NAMES={}
    freq={}
    l=[]

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
        self.l.append('{')
        for child in node.children:
            self.visit(child)

        see=[]
        while self.l[-1] != '{':
            see.append(self.l[-1])
            self.l.pop()
        self.l.pop()
        
        remove=[]
        for i,k in self.GLOBAL_SCOPE.items():
            if self.freq[i]==1 and i in see:
                remove.append(i)

        #print(remove)
        for i in remove:

            del self.GLOBAL_SCOPE[i]
            del self.freq[i]

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        val = self.visit(node.right)
        if(var_name in self.GLOBAL_FUNC_NAMES):
            raise Exception('There is a function with the same name')
        else:
            self.GLOBAL_SCOPE[var_name] = val
            if(var_name not in self.l): 
                self.l.append(var_name)
                if(var_name in self.freq): self.freq[var_name]+=1
                else: self.freq[var_name] = 1
    
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

        for n in node.elseif_nodes:
            ok = self.visit(n)
            if ok:
                return
        
        self.visit(node.else_body)

    def visit_ElseIfBlock(self, node):
        if self.visit(node.cond):
            self.visit(node.body)
            return 1

    def visit_ForBlock(self, node):
        self.visit(node.assign)
        while self.visit(node.cond):
            self.visit(node.body)
            self.visit(node.change)

    def visit_Print(self, node):
        for n in node.content:
            if(type(n)==str):
                print(n,end="")
            elif(type(n)==NoOp):
                pass
            else:
                print(self.visit(n),end="")
    
    def visit_Call(self, node):
        self.visit(self.GLOBAL_FUNC_NAMES[node.name])

    def visit_Func(self,node):
        return self.visit(node.body)

    def interpret(self):
        tree = self.parser.parse()
        for n in tree:
            self.GLOBAL_FUNC_NAMES[n.name]=n;

        self.visit(self.GLOBAL_FUNC_NAMES["MAIN"])