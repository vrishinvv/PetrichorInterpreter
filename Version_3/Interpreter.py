
###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################
from Parser import *
import io
import sys
old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout

class NodeVisitor(object):
    gf = 0
    ans = 0
    def visit(self, node, ret=[]):
        if(self.gf==1 and type(node).__name__ != "Compound"):
            # If the type was Compound, we want to enter it, so that we can erase the local variables 
            return self.ans
        
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        
        if(type(node).__name__ == "Compound"): 
            # we want to make the compound statement declare the variables 
            # after its '{' brackets is called, to make the paramteres local to the function
            return visitor(node,ret)
        else: 
            return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    GLOBAL_SCOPE={}
    GLOBAL_FUNC_NAMES={}
    CUR_FUNC=""
    freq={}
    l=[]

    def __init__(self, parser):
        self.parser = parser
        res=""

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
        else:
            raise Exception('Invalid operator')

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node,ret=[]):
        self.l.append('{')

        for i in ret:
            self.visit(i)

        for child in node.children:
            self.visit(child)
            if(self.gf): 
                break

        see=[]
        while self.l[-1] != '{':
            see.append(self.l[-1])
            self.l.pop()
        self.l.pop()
        
        remove=[]
        #print(self.l,see,remove)
        for i,k in self.GLOBAL_SCOPE.items():
            if self.freq[i]==1 and i in see:
                remove.append(i)

        for i in remove:
            del self.GLOBAL_SCOPE[i]
            del self.freq[i]

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        val = self.visit(node.right)
        if(var_name in self.GLOBAL_FUNC_NAMES):
            self.parser.lexer.err.res.append(' Invalid Function Naming -- COMPILE TIME ERROR'
                                            +'\n      There is a function with the same name'
                                            +'\n      At line:    '+str(node.left.token.line)
                                            +'\n      Wrong char: '+node.left.token.value
                                            )
        else:
            self.GLOBAL_SCOPE[var_name] = val
            see=[]
            t=self.l[:]
            while t[-1] != '{':
                see.append(t[-1])
                t.pop()
            t.pop()

            if(var_name not in see): 
                self.l.append(var_name)
                if(var_name in self.freq): 
                    self.freq[var_name]+=1
                else: 
                    self.freq[var_name] = 1
    
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
        self.GLOBAL_FUNC_NAMES[node.name].val_param = node.val_param
        self.gf=0
        self.visit(self.GLOBAL_FUNC_NAMES[node.name])
        self.gf=0
        return self.ans

    def visit_Return(self, node):
        self.ans = self.visit(node.value)
        self.gf = 1
        if(self.ans>=0): return
        if node.value in self.GLOBAL_SCOPE : self.ans = self.GLOBAL_SCOPE[node.value]
        else: self.ans = 0;
        return 

    def visit_Func(self,node):
        self.CUR_FUNC = node.name
        ret = []
        for i in range(len(node.var_param)):
            ret.append(Assign(node.var_param[i],Token('ASSIGN','ASSIGN'),node.val_param[i]))
    
        val = self.visit(node.body, ret)
        return val


    def interpret(self):
        tree = self.parser.parse()
        for n in tree:
            self.GLOBAL_FUNC_NAMES[n.name]=n;

        self.l.append('{')
        if("MAIN" not in self.GLOBAL_FUNC_NAMES):
            self.parser.lexer.err.res.append(' Invalid Function Naming -- COMPILE TIME ERROR\n'
                +'      Main Function does not exist') 
        else:
            self.GLOBAL_FUNC_NAMES["MAIN"].val_param.append(NoOp())
            self.visit(self.GLOBAL_FUNC_NAMES["MAIN"])
            self.res=new_stdout.getvalue()

        sys.stdout = old_stdout
        errObj=self.parser.lexer.err
        if(len(errObj.res)==0):
            print(self.res)
            print('-- Compiled SUCCESSFULLY with 0 errors!!!')
        else:
            print('-- Compiled UN-SUCCESSFULLY with '+str(len(errObj.res))+' error(s)!!!')
            for i in range(len(errObj.res)):
                print(i+1,": ")
                print(errObj.res[i])
            print()
