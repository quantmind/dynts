from dynts.dsl.grammar import *
from dynts.exceptions import DyntsException
from dynts.backends import istimeseries
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
    
    def unwind(self):
        if not hasattr(self,'_ts'):
            self._unwind()
        return self
    
    def ts(self):
        self.unwind()
        return self._ts
    
    def xy(self):
        self.unwind()
        return self._xy
        
    def _unwind(self):    
        res = self.expression.unwind(self.data,object())
        self._xy = None
        if istimeseries(res):
            self._ts = res
        elif res and isinstance(res,list):
            ts = None
            for r in res:
                if istimeseries(r):
                    if ts is None:
                        ts = r
                    else:
                        ts = ts.merge(r)
            self._ts = ts
        else:
            self._ts = None
            
    def toflot(self):
        ts = self.ts()
        xy = self.xy()
        if ts:
            flot = ts.dump('json')
        else:
            flot = None
        if xy:
            pass
        return flot
            
        
