from dynts.dsl.grammar import *
from dynts.conf import settings
from dynts.exceptions import DyntsException
from dynts.backends import istimeseries
from dynts.dsl.registry import FunctionBase, function_registry
from dynts.utils import smart_str


def parse(timeseries_expression, method = None, functions = None):
    '''Function for parsing :ref:`timeseries expressions <dsl-script>`.
If succesful, it returns an instance of :class:`dynts.dsl.Expr`.'''
    from ply import yacc
    from rules import rules
    functions = functions if functions is not None else function_registry
    ru = rules(functions)
    ru.build()
    ru.input(smart_str(timeseries_expression).lower())
    tokens     = ru.tokens
    precedence = ru.precedence
    yacc       = yacc.yacc(method = method or 'SLR')
    return yacc.parse(lexer = ru.lexer)


def merge(series):
    '''Merge timeseries. *series* must be an iterable over
timeseries.'''
    series = iter(series)
    ts = series.next()
    return ts.merge(series)

    
class dslresult(object):
    
    def __init__(self, expression, data, backend = None):
        self.expression = expression
        self.data = data
        self.backend = backend or settings.backend
        
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
        res = self.expression.unwind(self.data,self.backend)
        self._xy = None
        if istimeseries(res):
            self._ts = res
        elif res and isinstance(res,list):
            self._ts = merge(res)
        else:
            self._ts = None
            
    def dump(self, format):
        ts = self.ts()
        xy = self.xy()
        if ts:
            ts = ts.dump(format)
        else:
            ts = None
        if xy:
            pass
        return ts
            
        
