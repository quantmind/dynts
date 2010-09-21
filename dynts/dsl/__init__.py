from dynts.dsl.grammar import *
from dynts.exceptions import DyntsException
from dynts.dsl.registry import FunctionBase, function_registry


def parse(timeseries_expression, method = None, functions = None):
    '''Function for parsing :ref:`timeseries expressions <dsl-script>`.
If succesful, it returns an instance of :class:`dynts.dsl.Expr`.'''
    from ply import yacc
    from rules import rules
    functions = functions if functions is not None else function_registry
    ru = rules(functions)
    ru.build()
    ru.input(str(timeseries_expression).lower())
    tokens     = ru.tokens
    precedence = ru.precedence
    yacc       = yacc.yacc(method = method or 'SLR')
    return yacc.parse(lexer = ru.lexer)

    
class dslresult(object):
    
    def __init__(self, expression, data):
        self.expression = expression
        self.data = data
        
    def __unicode__(self):
        return u'%s' % self.expression
    
    def __repr__(self):
        return self.expression.__repr__()
    
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
        
        
    
    
    
