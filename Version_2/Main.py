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
                FUNC TEST(){
                    n=10;
                    x=100000000;
                    FOR(i=1;i<=n;i=i+1;){
                        FOR(j=1; j<=n; j=j+1;){
                            PRINT(i,",",j," ",)
                        }
                        PRINT("\n",)
                        x=x-1;
                    }
                    x=x-10;
                    y=10;

                }

                FUNC MAIN(){
                    CALL TEST();
                    n=8;
                    x=4;
                    FOR(i=1;i<=n;i=i+1;){
                        FOR(j=1; j<=n; j=j+1;){
                            PRINT(i,",",j," ",)
                            a=10;
                            b=10;
                        }
                        PRINT("\n",)
                    }
                    PRINT(x,"\n",)

                }
                 """

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()

        print(interpreter.GLOBAL_SCOPE.get('hello'))
        break


if __name__ == '__main__':
    main()

