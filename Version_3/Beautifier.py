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

    def pad(self,ok):
        if self.current_char == '}' and  ok==0: 
            self.cur_depth-=1

        if self.peek() == '}' and  ok==1: 
            self.cur_depth-=1

        for i in range(self.cur_depth):
            self.res+='   '

        if self.current_char == '}' and ok==0: 
            self.cur_depth+=1

        if self.peek() == '}' and  ok==1: 
            self.cur_depth+=1



    def skip_whitespace(self):
        # as the name suggests, it skips the white spaces
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def solve(self):
        quo=0
        self.skip_whitespace()
        self.pad(0)
        while self.current_char is not None:
            ok=0
        
            if(self.current_char == '"'): quo ^= 1;
            if(self.current_char == '\n' and quo==1):
                self.res += '\\n'
                self.advance()
                continue

            if(self.current_char in [';','{','}'] and quo==1):
                self.res += self.current_char
                self.advance()
                continue

            self.res+=str(self.current_char)
            if self.current_char not in ['{','}',';']:
                if(self.current_char =='\n'): 
                    self.advance()
                    self.skip_whitespace()
                    self.pad(ok)
                else:
                    self.advance()
                continue
                
            
            # cur_char is '}' or '{' or ';'
            if self.peek() != '\n':
                self.res+='\n'
                ok=1;

            if self.current_char == '{':
                self.cur_depth += 1
            if self.current_char == '}': 
                self.cur_depth-=1
            
            self.pad(ok)
            self.advance()

        return self.res
