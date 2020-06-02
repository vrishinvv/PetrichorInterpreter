from Interpreter import * 
from Beautifier import *
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
                FUNC TEST(n,x,y,){
                    FOR(i=1, i<=n, i=i+1,){
FOR(j=1, j<=n, j=j+1,){
     PRINT(i,",",j," ",);
                        }
            PRINT("\n",);
                    }
                }

                FUNC recur(n,){
                    IF(n==1){RETURN 1;}
                    RETURN n+CALL recur(n-1,);
                }


                FUNC MAIN(){
                    b=6;
                    a=CALL recur(4,);
                    FOR(i=1,i<=b,i=i+1,){
                        PRINT(i,": ",CALL recur(i,),"\n",);
                    }
                    PRINT(a,"\n;",);
                    CALL TEST(4,5,5,);
                }
                 """

        Beautifier = Beautify(text)
        print(str(Beautifier.solve()))
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()
        break


if __name__ == '__main__':
    main()

