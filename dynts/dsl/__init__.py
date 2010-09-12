from dynts.dsl.grammar import *

registered_functions = {}

def parse(input, method = 'SLR'):
    '''Function for parsing input string'''
    from ply import yacc
    from rules import rules
    ru = rules(registered_functions)
    ru.build()
    ru.input(str(input).lower())
    tokens     = ru.tokens
    precedence = ru.precedence
    yacc       = yacc.yacc(method = method)
    return yacc.parse(lexer = ru.lexer)
    
