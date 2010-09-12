from dynts.conf import settings
from dynts import timeserie, istimeserie
from dynts.dsl.ast.errors import *

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
        return 1
    
    def __unicode__(self):
        return u'%s' % self.info()
    
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
        '''Return a list of :ref:`Symbol <dsl-symbol>` instances.'''
        return None
    
    def variables(self):
        '''Return a list of :ref:`Variable <dsl-symbol>` instances.'''
        return None
    
    def removeduplicates(self, entries = None):
        return None
    
    def json(self, values, unwind):
        ts = self.unwind(values, unwind)
        return ts.json()
        
    def apply(self, values):
        ts = self.unwind(values)
        return ts.apply()
    
    def unwind(self, values, unwind, **kwargs):
        if not hasattr(self, "_unwind_value"):
            self._unwind_value = self._unwind(values, unwind, **kwargs)
        return self._unwind_value
    
    def _unwind(self, values, unwind, **kwargs):
        raise NotImplementedError("Unwind method missing for %s" % self)
    
    def lineardecomp(self):
        return None
    

class BaseExpression(Expr):
    '''Base class for single-value expression
    '''
    def __init__(self, value):
        self.value = value
        
    def info(self):
        return str(self.value)
        
    
class Expression(BaseExpression):
    '''Base class for single expression
    '''
    def __init__(self, value):
        super(Expression,self).__init__(value)
        
    def info(self):
        return str(self.value)
    
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
        
    def _unwind(self, values, unwind, **kwargs):
        return self.value


class String(BaseExpression):
    '''
    A simple string.
    This expression is a constant numeric value
    '''
    def __init__(self,value):
        super(String,self).__init__(str(value))
        
    def _unwind(self, values, unwind, **kwargs):
        return unwind.stringData(self.value)


class Symbol(BaseExpression):
    '''Timeserie symbol. This expression is replaced by a timeserie value for the symbol
    '''
    def __init__(self, value, field = None):
        super(Symbol,self).__init__(value)
    
    def symbols(self):
        return [str(self)]
    
    def _unwind(self, values, unwind, **kwargs):
        sdata = values[str(self)]
        if istimeserie(sdata):
            return sdata
        else:
            ts = timeserie(self, date = sdata['date'], data = sdata['value'])
            values[str(self)] = ts
            return ts
    
    def lineardecomp(self):
        return linearDecomp().append(self)


class MultiExpression(Expr):
    '''
    Base class for expression involving two or more elements
    '''
    def __init__(self, concat_operator, concatenate = True):
        self.__concatenate   = concatenate
        self.children        = []
        self.concat_operator = concat_operator
        
    def __len__(self):
        return len(self.children)
    
    def __iter__(self):
        return self.children.__iter__()
        
    def internal_info(self):
        cs = None
        for c in self.children:
            if cs == None:
                cs = '%s' % c
            else:
                cs += ' %s %s' % (self.concat_operator,c)
        return cs
    
    def info(self):
        return self.internal_info()
    
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
        
    def _unwind(self, values, unwind, sametype = True, **kwargs):
        result = []
        for child in self:
            result.append(child.unwind(values, unwind))
        return result
    
    
class SplittingOp(ConcatOp):
    
    def __init__(self,left,right):
        super(SplittingOp,self).__init__(left, right, settings.separator_operator)
        
    def _unwind(self, values, unwind, **kwargs):
        ts = unwind.listData(label = str(self))            
        for c in self:
            v = c.unwind(values, unwind)
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
    
    def __init__(self,left,right):
        super(EqualOp,self).__init__(left,right,"=")
        if not isinstance(self.left,Symbol):
            raise ValueError('Left-hand-side of %s should be a Symbol' % self)
    
    def _unwind(self, values, unwind, **kwargs):
        data = self.right.unwind(values, unwind, **kwargs)
        return unwind.keyValue(str(self.left), data.data)
    
    def symbols(self):
        return self.right.symbols()
 
 
class Bracket(Expression):
    
    def __init__(self,value,pl,pr):
        self.__pl = pl
        self.__pr = pr
        super(Bracket,self).__init__(value)
        #self._process(value)
    
    def info(self):
        return '%s%s%s' % (self.__pl,self.value,self.__pr)
    
    def _process(self,value):
        if self.concat_operator == None:
            self.children.append(value)
        else:
            if self.isconcatoper(value):
                cs = value.children
                for c in cs:
                    self._process(c)
            else:
                self.childrens.append(value)
                
    
        
class uMinus(Expression):
    def __init__(self,value):
        Expression.__init__(self,value)
        
    def info(self):
        return '-%s' % self.value
    
    def lineardecomp(self):
        return linearDecomp().append(self,-1)
    