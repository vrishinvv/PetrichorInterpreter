"""
Token types / constants
"""

# Data Type
INTEGER            =   'INTEGER'

# Operators
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

# Key Words
BEGIN              =   '{'
END                =   '}'
IF                 =   'IF'
FI                 =   'FI'
ELSE               =   'ELSE'
ELSEIF             =   'ELSEIF'
FOO                =   'FOO'
PRINT              =   'PRINT'
FOR                =   'FOR'
FUNC               =   'FUNC'
CALL               =   'CALL'
RETURN             =   'RETURN'

#Misc Tokens
SEMI               =   'SEMI'
DOT                =   'DOT'
ASSIGN             =   'ASSIGN'
ID                 =   'ID'
STR                =   'STR'
COMMA              =   ','

class Error:
    def __init__(self):
        self.res=[]

class Token(object):
    def __init__(self, type, value,line=0):
        self.type = type
        self.value = value
        self.line = line

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
    'PRINT': Token('PRINT', 'PRINT'),
    'FOR'  : Token('FOR', 'FOR'),
    'FUNC'  : Token('FUNC', 'FUNC'),
    'CALL'  : Token('CALL', 'CALL'),
    'RETURN'  : Token('RETURN', 'RETURN'),
}