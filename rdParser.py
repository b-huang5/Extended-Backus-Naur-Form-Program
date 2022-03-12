#CS530 T/Th 11:00-12:15
# Single Programmer Affidavit
# I the undersigned promise that the attached assignment is my own work. While I was free to discuss ideas with others, the work contained 
#is my own. I recognize that should this not be the case, I will be subject to penalties as outlined in the course syllabus. 
# Your Name Here
#Brian Huang
#Red ID: 822761804
#11/30/21

import re
from functools import *

"""

Assignment 2 - 
A LL(1) recursive descent parser for validating simple expressions.

# Task A:
You would need to first write the grammar rules (non-terminal) in EBNF 
according to the token patterns and grammar rules specified in the prompt,
put the rules in a separate PDF file, see prompt. 
(Refer to the EBNF example in Figure 5.15)

# Task B:
You would then write the recursive descent parsing procedures for the 
validation parsing according to the rules from Task A. 
(Refer to the parsing algorithm in Figure 5.17)

It implements one parsing procedure for each one of the 
non-terminals (grammar rules), starting from the top of the parse tree, 
then drilling into lower hierachical levels.

The procedures work together to handle all combinations of the grammar 
rules, and they automatically handle the nested compositions of terms 
with multi-level priority brackets. 

----------------------------------------------------------------------------
Usage (Refer to the prompt for more examples - both positive and negative cases)

r = recDecsent('7 - 17')
print(r.validate()) # will print True as '7 - 17' is a valid expression

r = recDecsent('7 - ')
print(r.validate()) # will print False as '7 - ' is an invalid expression

"""

class recDescent: 

    count = 0
    parenthesis = 0
    # IMPORTANT:
    # You MUST NOT change the signatures of 
    # the constructor, lex(self) and validate(self)
    # Otherwise, autograding tests will FAIL

    # constructor to initialize and set class level variables
    def __init__(self, expr = ""):

        # string to be parsed
        self.expr = expr

        # tokens from lexer tokenization of the expression
        self.tokens = []

    # lexer - tokenize the expression into a list of tokens
    # the tokens are stored in an list which can be accessed by self.tokens
    # do not edit any piece of code in this function
    def lex(self):
        self.tokens = re.findall("[-\(\)=]|[!<>]=|[<>]|\w+|[^ +]\W+", self.expr)
        # transform tokens to lower case, and filter out possible spaces in the tokens
        self.tokens = list(filter((lambda x: len(x)), 
                           list(map((lambda x: x.strip().lower()), self.tokens))))    
    
    # parser - determine if the input expression is valid or not
    
    # validate() function will return True if the expression is valid, False otherwise 
    # do not change the method signature as this function will be called by the autograder
    def validate(self):
        # Using the tokens from lex() tokenization,
        # your validate would first call lex() to first tokenize the expression
        # then call the top level parsing procedure and go from there
        self.lex()
        return self.exp()
        pass

    # parsing procedures corresponding to the grammar rules - follow Figure 5.17

    def exp(self):
        found = False
        if(self.term()): # <term> {<op> <term>}
            found = True
            if(self.count < len(self.tokens)): #boundary checker
                if(self.parenthesis <= 0 and self.tokens[self.count] == ')'): #checks if extra ')'
                    found = False
                elif(self.tokens[self.count] == ')'): # "pops" '(' if a ')' is found
                    self.parenthesis -= 1
                    self.count += 1
                while(self.count < len(self.tokens) and found and self.logicalOperators(self.tokens[self.count])): # {<op> <term>}
                    self.count += 1
                    if( not( self.term() ) ):
                        found = False
                if(self.count < len(self.tokens) and self.tokens[self.count] == ')'): #if after the ')' is not the end program will continue
                    self.parenthesis -= 1
                    self.count += 1
                elif(self.count < len(self.tokens)): #if there's no <op> in between <term> but still continues
                    found = False
        
        if(found):
            if(self.parenthesis > 0): #checks if extra '('
                return False
            return True
        else:
            return False


    def term(self):
        found = False
        if(self.count < len(self.tokens)):#boundary checker
            if(self.tokens[self.count].isnumeric()): # int <dash> int
                self.count += 1
                if(self.count < len(self.tokens)): #boundary checker
                    found = True
                    if(self.dash(self.tokens[self.count])): # checks '-'
                        self.count += 1
                        if(self.count < len(self.tokens)): #boundary checker
                            if( not (self.tokens[self.count].isnumeric()) ): #if not int return false
                                found = False
                            else:
                                self.count += 1
                        else: # "1 -" error
                            found = False

            elif(self.relationalOperators(self.tokens[self.count])): # <relop> int
                self.count += 1
                if(self.count < len(self.tokens)): #boundary checker ("<" error)
                    found = True
                    if( not (self.tokens[self.count].isnumeric()) ): #if not int return false
                        found = False
                    else:
                        self.count += 1

            elif(self.tokens[self.count] == '('): # (<exp>)
                self.count += 1
                if(self.count < len(self.tokens)): #boundary checker ( "(" error)
                    self.parenthesis += 1
                    found = self.exp()
            
        if(found):
            return True
        else:
            return False

    def dash(self,d):
        return d == '-'


    def relationalOperators(self,op):
        ops = ["<", ">", "<=", ">=", "=", "!=", "not"]
        for i in ops:
            if(i == op):
                return True
        return False

    def logicalOperators(self, lo):
        los = ["and", "or", "nand", "xor", "xnor"]
        for i in los:
            if(i == lo):
                return True
        return False


if __name__ == "__main__":
    #true
    r = recDescent('1 - 17')
    print(r.validate())
    r = recDescent('> 90')
    print(r.validate())
    r = recDescent('(1 - 100 and not 50) or > 200')
    print(r.validate())
    r = recDescent('(7 - 17) or > 90')
    print(r.validate())
    r = recDescent('> 50 or = 20')
    print(r.validate())
    r = recDescent('1 - 100 and != 50')
    print(r.validate())
    r = recDescent('(5 - 100) and (not 50) or (>= 130 or (2 - 4))')
    print(r.validate())
    # false
    r = recDescent('>')
    print(r.validate())
    r = recDescent('2 - - 4')
    print(r.validate())
    r = recDescent('- 7')
    print(r.validate())
    r = recDescent('7 -')
    print(r.validate())
    r = recDescent('(!= 5) and')
    print(r.validate())
    r = recDescent('2 - 4 and > < 300')
    print(r.validate())
    r = recDescent('>= 5) xnor < 10')
    print(r.validate())

    