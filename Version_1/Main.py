from Interpreter import * 

def main():
    while True:
        # try:
        #     try:
        #         text = raw_input('spi> ')
        #     except NameError:  # Python3
        #         text = input('spi> ')
        # except EOFError:
        #     break
        # if not text:
        #     continue
        text = text = """\
                {
                    number = 2523*10;
                    x = 11;
                    IF(x<=11){
                        hello=2;
                        hello=hello-2;
                        a=0;
                        IF(a<1){
                            hello=108;
                        }ELSEIF(a<2){
                            hello=109;
                        }ELSEIF(a<3){
                            hello=110;
                        }ELSEIF(a<4){
                            hello=111;
                        }ELSEIF(a<5){
                            hello=112;
                        }ELSE{
                            hello=113;
                        }


                        FOR(i=2;i<=10;i=i+2;){
                            PRINT("Hello World!",)
                        }
                    }
                }
                 """

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
        print(interpreter.GLOBAL_SCOPE.get('hello'))
        break


if __name__ == '__main__':
    main()
