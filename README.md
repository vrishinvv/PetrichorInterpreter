# Petrichor_Interpreter

A **NEW** Programming language, that was created by combining the best of C++ and Python 3. 
*Totally built from scratch* wihout using any dependecies or libraries

~Still under development. 

### Interpeter can understand:
- [x] Basic statments
- [x] Complex mathematical expressions
- [x] If-Elseif-Else construct
- [x] For-Loop construct
- [x] Methods/Function
- [x] Parameterised Functions
- [x] Return Values

### Unique Features:
* **Local NameSpace handling** is inbuilt
* **'Recursion is possible'**, as you may have already guessed
* **'Error Description Package'** built into the tool
* Comes with a sleek **'Auto-Indendation'** feature

### Features in future udpates:
1. Expanding numbers to hold more than just an integer 
2. Key Words will be allowed to be given in small-letter as well

### Later Updates:
1. A good clean WebUI, to test Petrichor in action

### DrawBacks:
1. Error finding tool, is'nt as finished and complete as one we see in modern 
  interpreters, but does a good enough job to impress
2. Arrays/ classes/ have not yet been implemented

# GRAMMAR
Currenly looks similar to the C++ style of code, however, the no data type feature of Python has been integrated.
I might update syntax of language in future versions

'''

      program:
          FUNC*
      func : 
          FUNC ID (param) compound_statement

      return:
          RETURN exp|empty 

      param: 
          empty|(expr COMMA)*

      compound_statement: 
          BEGIN statement_list END

      statement_list : 
          (
                assignment_statement 
              | empty
              | if_block
              | print 
              | for_block
              |expr
              |return 
          )*

      assignment_statement : 
          variable ASSIGN expr 

      empty :

      print : 
          PRINT( ((str|expr)COMMA)*  )  

      call : 
          CALL ID (param)

      if_block: 
          IF expr 
              compound_statement 
          | (ELSEIF
              compound_statement)*
          | ELSE
              compount_statement
          | empty


      elseif_block:
          ELSEIF expr 
              compound_statement 

      for_block: 
          FOR(assignment_statement; cond; change) 
              compounf_statement


      factor :
           PLUS factor
         | MINUS factor
         | INTEGER
         | LPAREN expr RPAREN
         | variable
         | call

      term: 
          factor (
                      (
                           MUL 
                          | DIV 
                          | LESS_THAN 
                          | LESS_THAN_EQUAL 
                          | EQUALS 
                          | GREATER_THAN 
                          | GREATER_THAN_EQUAL
                      ) 
                  factor  
                  )*

      expr: 
          term (
                  (
                        PLUS 
                      | MINUS
                  ) 
               term
               )*


      variable: 
          ID 
'''

# RULES
* Variables declared within a 'compound_statement' are local to that compound_statement
* redeclaring / aka reinitialising a variable inside a compound_statement(CS) will be considered as updation ONLY
* As of now, string objects cannot be assigned to variables, they take up ONLY integers
* There must be a "MAIN" function, Yes in caps, in your program
