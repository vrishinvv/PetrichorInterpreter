
###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################
from Helper import * 
# Token
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
    'PRINT': Token('PRINT', 'PRINT'),
    'FOR'  : Token('FOR', 'FOR'),
    'FUNC'  : Token('FUNC', 'FUNC'),
    'CALL'  : Token('CALL', 'CALL'),
    'RETURN'  : Token('RETURN', 'RETURN'),
}

# Lexer
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def peek(self):
        # peeks one pos ahead, and returns the charcter there
        # wihtout actually moving the pos pointer 
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def advance(self):
        # moves the pos pointer one step ahead
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # as the name suggests, it skips the white spaces
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        """ Handle identifiers and reserved keywords """
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token


    def integer(self):
        """ Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_str(self):
        """ Return a string from the input """
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char is not "\"":
            result += self.current_char
            self.advance()
        self.advance()
        return str(result)


    def get_next_token(self):
        """ Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self.current_char is not None:

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '"':
                return Token(STR, self.get_str())

            if self.current_char == ',':
                self.advance()
                return Token(COMMA,',')

            if self.current_char == '{':
                self.advance()
                return Token(BEGIN, '{')

            if self.current_char == '}':
                self.advance()
                return Token(END, '}')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(EQUALS, '==')

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

