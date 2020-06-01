# Token types
INTEGER           =   'INTEGER'
PLUS              =   'PLUS'
MINUS             =   'MINUS'
MULT              =   'MULT'
DIV               =   'DIV'
EOF               =   'EOF'

def is_operator(c):
    return c in ['+','-','*','/']

def recognise_operator(c):
    switcher ={
        '+':  PLUS,
        '-':  MINUS,
        '*':  MULT,
        '/':  DIV
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

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

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

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if is_operator(self.current_char):
                t = Token(recognise_operator(self.current_char),self.current_char)
                self.advance()
                return t

            self.error()

        return Token(EOF, None)

class Interpreter(object):
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
        """Return an INTEGER token value."""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """Arithmetic expression parser / interpreter.

        expr   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.factor()

        while is_operator(self.current_token.value):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.factor()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.factor()
            elif token.type == MULT:
                self.eat(MULT)
                result = result * self.factor()
            else:
                self.eat(DIV)
                result = result / self.factor()
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()