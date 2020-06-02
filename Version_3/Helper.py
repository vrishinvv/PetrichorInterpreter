from Constants import *
# helper functions
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


class Error:
    def __init__(self):
        self.res=[]
