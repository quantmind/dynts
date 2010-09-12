from dynts.dsl.grammar import *
from dynts.exceptions import DyntsException
from dynts.data import dynts_providers

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

    
class dslresult(object):
    
    def __init__(self, expression, data):
        self.expression = expression
        self.data = data
        
    def __unicode__(self):
        return u'%s' % self.expression
    
    def __repr__(self):
        return '%s' % self.expression
    
    def __str__(self):
        return self.__repr__()
    
    def unwind(self):
        unwind = object()
        return self.expression.unwind(self.data,unwind)
        
        
    
    
    
