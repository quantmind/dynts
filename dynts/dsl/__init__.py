'''A domain specific language for timeseries analysis and manipulation.

Created using ply (http://www.dabeaz.com/ply/) a pure Python implementation
of the popular compiler construction tools lex and yacc.
'''
from dynts.conf import settings
from dynts.dsl.grammar import *
from dynts.exceptions import DyntsException
from dynts.backends import istimeseries, isxy
from dynts.dsl.registry import FunctionBase, ComposeFunction, function_registry
from dynts.utils import smart_str


def parse(timeseries_expression, method = None, functions = None, debug = False):
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
    return yacc.parse(lexer = ru.lexer, debug = debug)


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
        self._ts = None
        self._xy = None
        if istimeseries(res):
            self._ts = res
        elif res and isinstance(res,list):
            tss = []
            xys = []
            for v in res:
                if istimeseries(v):
                    tss.append(v)
                elif isxy(v):
                    xys.append(v)
            if tss:
                self._ts = merge(tss)
            if xys:
                self._xy = xys
        elif isxy(res):
            self._xy = res
            
    def dump(self, format, **kwargs):
        ts = self.ts()
        xy = self.xy()
        if istimeseries(ts):
            ts = ts.dump(format, **kwargs)
        else:
            ts = None
        if xy:
            if isxy(xy):
                xy = [xy]
            for el in xy:
                ts = el.dump(format, container = ts, **kwargs)
        return ts
            
        
