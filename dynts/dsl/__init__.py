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
    
    def unwind(self, format = None):
        unwind = object()
        ts = self.expression.unwind(self.data,unwind)
        if format is None:
            return ts
        elif format.lower() == 'flot':
            return self.toflot(ts)
        else:
            return ts
        
    def toflot(self, ts):
        from dynts.web import flot
        res = flot.Flot()
        result = flot.MultiPlot(res)
        if not isinstance(ts,list):
            ts = [ts]
        for serie in ts:
            data = []
            for dt,val in serie.items():
                data.append([flot.pydate2flot(dt),val])
            serie = flot.Serie(label = serie.name, data = data)
            res.add(serie)
        return result
        
        
    
    
    
