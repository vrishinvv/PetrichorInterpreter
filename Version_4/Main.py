from Interpreter import * 
from Beautifier import *

def main():    
    text = """\
            FUNC TEST(n,x,y,){
                FOR(i=1, i<=n, i=i+1,){
                    FOR(j=1, j<=n, j=j+1,){
                        PRINT(i,",",j," ",);
                    }   
                    PRINT("\n",);
                }
            }

            FUNC recur(n,){
                IF(n==1){
                    RETURN 1;
                }RETURN n+CALL recur(n-1,);
            }

            FUNC MAIN(){CALL TEST(4,2,3,); n=4;a=5;    FOR(i=1,i<=n,i=i+1,){PRINT(i,": ",CALL recur(i,),"\n",);}                    PRINT(a,"\n;",);}
            """

    Beautifier = Beautify(text)
    res=Beautifier.solve()
    print(res)
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


if __name__ == '__main__':
    main()


"""
Output:
FUNC TEST(n,x,y,){
   FOR(i=1, i<=n, i=i+1,){
      FOR(j=1, j<=n, j=j+1,){
         PRINT(i,",",j," ",);
      }
      PRINT("\n",);
   }
}
FUNC recur(n,){
   IF(n==1){
      RETURN 1;
   }
   RETURN n+CALL recur(n-1,);
}
FUNC MAIN(){
   CALL TEST(4,2,3,);
   n=4;
   a=5;
   FOR(i=1,i<=n,i=i+1,){
      PRINT(i,": ",CALL recur(i,),"\n",);
   }
   PRINT(a,"\n;",);
}

1,1 1,2 1,3 1,4 
2,1 2,2 2,3 2,4 
3,1 3,2 3,3 3,4 
4,1 4,2 4,3 4,4 
1: 1
2: 3
3: 6
4: 10
5
;
-- Compiled SUCCESSFULLY with 0 errors!!!
"""
    
