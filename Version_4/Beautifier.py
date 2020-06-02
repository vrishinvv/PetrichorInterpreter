###############################################################################
#                                                                             #
#  BEAUTIFIER                                                                 #
#                                                                             #
###############################################################################

class Beautify:
    def __init__(self, text):
        self.text=text
        self.pos=0
        self.cur_depth=0;
        self.current_char = self.text[self.pos]
        self.res=""

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

    def pad(self):
        # if the current char is a closing bracket
        # we have to artficially decrease depth before padding
        if self.current_char == '}': 
            self.cur_depth -= 1

        for i in range(self.cur_depth):
            self.res+='   '

        # we have to artficially restore depth after padding
        if self.current_char == '}': 
            self.cur_depth += 1



    def skip_whitespace(self):
        # as the name suggests, it skips the white spaces
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def special_case_handle(self,quo):
        # special handling to print \n as \n
        if(self.current_char == '\n' and quo==1):
            self.res += '\\n'
            self.advance()
            return 1

        # special handling to print special characters within quotes
        if(self.current_char in [';','{','}'] and quo==1):
            self.res += self.current_char
            self.advance()
            return 1

        return 0

    def solve(self):
        # variable to keep track, if im within quotes or not
        quo=0
        # initiallising my pointer to the first non_space character in input 
        self.skip_whitespace()
        self.pad()

        # loop until EOF
        while self.current_char is not None:
            #updating if im within a quotes range
            if self.current_char == '"': 
                quo ^= 1;

            if self.special_case_handle(quo):
                continue

            # add current (whatever it may be) character to res
            self.res+=str(self.current_char)
            # handling normal characters
            if self.current_char not in ['{','}',';']:
                if(self.current_char =='\n'): 
                    self.advance()
                    self.skip_whitespace()
                    self.pad()
                else:
                    self.advance()
                continue
                
            
            # cur_char is '}' or '{' or ';'
            if self.current_char == '{':
                self.cur_depth += 1
            if self.current_char == '}': 
                self.cur_depth -= 1

            # if the next character is '\n', then great, no need to do anything
            # if not, then special handling is required, as follows
            if self.peek() != '\n':
                self.res+='\n'
                self.advance()
                self.skip_whitespace()
                self.pad()
                continue

            # step statement of while loop
            self.advance()

        return self.res
