from dynts.conf import settings
from dynts import timeseries, istimeseries, ts_bin_op
from dynts.exceptions import *

def isnumber(value):
    try:
        float(value)
        return True
    except:
        return False

class Expr(object):
    '''Base class for abstract syntax nodes
    '''    
    def count(self):
        '''Number of nodes'''
        return 1
    
    def malformed(self):
        return False
    
    @property
    def type(self):
        return self.__class__.__name__.lower()
    
    def info(self):
        return ''
    
    def __repr__(self):
        return '%s' % self.info()
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        return isinstance(other, Expr) and str(other) == str(self)
    
    def symbols(self):
        '''Return a list of :class:`dynts.dsl.Symbol` instances.'''
        return None
    
    def variables(self):
        return None
    
    def removeduplicates(self, entries = None):
        return None
    
    def unwind(self, values, backend, **kwargs):
        '''Unwind expression by applying *values* to the abstract nodes.
the ``kwargs`` dictionary can contain data which can be used to override values'''
        if not hasattr(self, "_unwind_value"):
            self._unwind_value = self._unwind(values, backend, **kwargs)
        return self._unwind_value
    
    def _unwind(self, values, backend, **kwargs):
        raise NotImplementedError("Unwind method missing for %s" % self)
    

class BaseExpression(Expr):
    '''Base class for single-value expression
    '''
    def __init__(self, value):
        self.value = value
        
    def info(self):
        return str(self.value)
        

class BadExpression(BaseExpression):
    '''A malformed expression
    '''
    def malformed(self):
        return True
    
    
class Expression(BaseExpression):
    '''Base class for single expression
    '''    
    def symbols(self):
        return self.value.symbols()
    
    def removeduplicates(self, entries = None):
        if entries == None:
            entries = {}
        if isinstance(self.value,Symbol):
            c = entries.get(str(self.value), None)
            if c:
                ov = [self.value]
                self.value = c
                return ov
            else:
                entries[str(self.value)] = self.value
                return None
        else:
            return self.value.removeduplicates(entries = entries)
    
    
class Number(BaseExpression):
    '''
    A simple number.
    This expression is a constant numeric value
    '''
    def __init__(self,value):
        super(Number,self).__init__(value)
        
    def _unwind(self, values, backend, **kwargs):
        return self.value


class String(BaseExpression):
    '''
    A simple string.
    This expression is a constant numeric value
    '''
    def __init__(self,value):
        super(String,self).__init__(str(value))
        
    def _unwind(self, values, backend, **kwargs):
        return unwind.stringData(self.value)


class Parameter(BaseExpression):
    
    def __init__(self, value):
        value = str(value).lower()
        super(Parameter,self).__init__(value)
        

class Symbol(BaseExpression):
    '''Timeserie symbol. This expression is replaced by a timeserie value for the symbol
    '''
    def __init__(self, value, field = None):
        value = settings.symboltransform(value)
        if len(value)>2 and value[0] == '`' and value[-1] == '`':
            self.quotes = True
            value = value[1:-1]
        else:
            self.quotes = False
        super(Symbol,self).__init__(str(value))
    
    def info(self):
        if self.quotes:
            return '`{0}`'.format(self.value)
        else:
            return self.value
        
    def symbols(self):
        return [self.value]
    
    def _unwind(self, values, backend, **kwargs):
        sdata = values[self.value]
        if istimeseries(sdata):
            return sdata
        else:
            ts = timeseries(name = str(self),
                            date = sdata['date'],
                            data = sdata['value'],
                            backend = backend)
            # Uses this hack to make sure timeseries are ordered
            # Lots of room for performance improvement
            hash = ts.ashash()
            hash.modified = True
            values[ts.name] = hash.getts()
            return ts
    
    def lineardecomp(self):
        return linearDecomp().append(self)


class MultiExpression(Expr):
    '''Base class for expression involving two or more elements
    '''
    def __init__(self, concat_operator, concatenate = True):
        self.__concatenate   = concatenate
        self.children        = []
        self.concat_operator = concat_operator
        
    def malformed(self):
        for child in self.children:
            if child.malformed():
                return True
        return False
    
    def __len__(self):
        return len(self.children)
    
    def __iter__(self):
        return self.children.__iter__()
        
    def info(self):
        c = self.concat_operator
        return reduce(lambda x,y: '%s%s%s' % (x,c,y),self.children)
    
    def symbols(self):
        cs = []
        for c in self.children:
            ns = c.symbols()
            if ns:
                for n in ns:
                    if n not in cs:
                        cs.append(n)
        return cs
    
    def append(self, el):
        if isinstance(el,self.__class__) and self.__concatenate:
            for c in el:
                self.append(c)
        elif isinstance(el,Expr):
            self.children.append(el)
        else:
            raise ValueError("%s is not a valid grammar expression" % el)
        return el
            
    def __getitem__(self, idx):
        return self.children[idx]
    
    def removeduplicates(self, entries = None):
        '''
        Loop over children a remove duplicate entries.
        @return - a list of removed entries
        '''
        removed      = []
        if entries == None:
            entries = {}
        new_children = []
        for c in self.children:
            cs = str(c)
            cp = entries.get(cs,None)
            if cp:
                new_children.append(cp)
                removed.append(c)
            else:
                dups = c.removeduplicates(entries)
                if dups:
                    removed.extend(dups)
                entries[cs] = c
                new_children.append(c)
        self.children = new_children
        return removed
            
            

class ConcatOp(MultiExpression):
    '''
    Refinement of MultiExpression with a new constructor.
    This class simply define a new __init__ method
    '''
    def __init__(self, left, right, op, concatenate = True):
        super(ConcatOp,self).__init__(op, concatenate = concatenate)
        self.append(left)
        self.append(right)
        


class ConcatenationOp(ConcatOp):
    
    def __init__(self,left,right):
        super(ConcatenationOp,self).__init__(left, right, settings.concat_operator)
        
    def _unwind(self, values, backend, sametype = True, **kwargs):
        result = []
        for child in self:
            result.append(child.unwind(values, backend, **kwargs))
        return result
    
    
class SplittingOp(ConcatOp):
    
    def __init__(self,left,right):
        super(SplittingOp,self).__init__(left, right, settings.separator_operator)
        
    def _unwind(self, values, backend, **kwargs):
        ts = unwind.listData(label = str(self))            
        for c in self:
            v = c.unwind(values, backend)
            ts.append(v)
        return ts

        
class BinOp(ConcatOp):
    
    def __init__(self,left,right,op):
        if op in settings.special_operators:
            raise ValueError('Conactentaion operator "%s" is not a valid binary operator' % op)
        super(BinOp,self).__init__(left, right, op, concatenate = False)
        self.append = None
        
    def __get_left(self):
        return self[0]
    left = property(fget = __get_left)
    
    def __get_right(self):
        return self[1]
    right = property(fget = __get_right)
    
    
class EqualOp(BinOp):
    '''Equal operator expression. For example
    
* ``window = 35``
* ``param = AMZN``

The left hand side is the name of the parameter, while the right-hand side
is the parameter values which can be a :class:`Symbol`.
The left hand side is **never** a symbol. 
'''
    def __init__(self,left,right):
        if not isinstance(left,Parameter):
            if not isinstance(left,Symbol):
                raise ValueError('Left-hand-side of %s should be a string' % self)
            left = Parameter(left.value)
        super(EqualOp,self).__init__(left,right,"=")
        
    def _unwind(self, values, backend, **kwargs):
        name = str(self.left)
        if name in kwargs:
            return {name:kwargs[name]}
        else:
            return {name:self.right.unwind(values, backend, **kwargs)}
 
 
class Bracket(Expression):
    '''A :class:`dynts.dsl.Expr` class for enclosing group of :class:`dynts.dsl.Expr`.
It forms the building block of :class:`dynts.dsl.Function` and other operators.'''
    def __init__(self,value,pl,pr):
        self.__pl = pl
        self.__pr = pr
        super(Bracket,self).__init__(value)
    
    def info(self):
        return '%s%s%s' % (self.__pl,self.value,self.__pr)
    
    def _unwind(self, *args, **kwargs):
        data = self.value.unwind(*args, **kwargs)
        if not isinstance(data,list):
            data = [data]
        args = []
        kwargs = {}
        for item in data:
            if isinstance(item,dict):
                kwargs.update(item)
            else:
                args.append(item)
        return args,kwargs
                
                
class uMinus(Expression):
    def __init__(self,value):
        Expression.__init__(self,value)
        
    def info(self):
        return '-%s' % self.value
    
    def lineardecomp(self):
        return linearDecomp().append(self,-1)
    