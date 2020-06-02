###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################
from Helper import * 

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 0
        self.col = 0
        self.current_char = self.text[self.pos]
        self.err = Error() 
    
    def error(self):
        self.err.res.append(' Invalid Token Used -- COMPILE TIME ERROR'
                        +'\n      Wrong char: '+self.current_char
                        +'\n      At line:    '+str(self.line)
                        +'\n      At char:    '+self.text[self.pos]
                        )
        self.advance()

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
        self.col += 1
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

        token = RESERVED_KEYWORDS.get(result, Token(ID, result,self.line))
        token.line = self.line
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
        """ 
        Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self.current_char is not None:

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '"':
                return Token(STR, self.get_str(),self.line)

            if self.current_char == '\n':
                self.advance()
                self.line+=1
                self.col=self.line
                continue

            if self.current_char == ',':
                self.advance()
                return Token(COMMA,',',self.line)

            if self.current_char == '{':
                self.advance()
                return Token(BEGIN, '{',self.line)

            if self.current_char == '}':
                self.advance()
                return Token(END, '}',self.line)

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(EQUALS, '==',self.line)

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=',self.line)

            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(LESS_THAN_EQUAL, '<=',self.line)

            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(GREATER_THAN_EQUAL, '>=',self.line)

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';',self.line)

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.',self.line)
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer(),self.line)

            if is_operator(self.current_char):
                t = Token(recognise_operator(self.current_char),self.current_char,self.line)
                self.advance()
                return t

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(',self.line)

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')',self.line)

            self.error()

        return Token(EOF, None,self.line)

