from dynts.dsl.ast.binmath import *

class Function(Bracket):
    '''A :class:`dynts.dsl.Bracket` representing a function *func*, an instance of :class:`dynts.dsl.FunctionBase`.
A function is defined a-la Python as::
    
    func(expression, **kwargs)
    
where *kwargs* is a dictionary of input parameters. For example, the rolling-standard deviation
is defined as::

    std(expression,window=20)
    '''
    
    def __init__(self, func, expression, pl, pr):
        self.func = func
        super(Function,self).__init__(expression, pl, pr)
            
    def info(self):
        return '{0}{1}'.format(self.func,super(Function,self).info())
    
    def _unwind(self, values, backend, **kwargs):
        args,kwargs = super(Function,self)._unwind(values, backend, **kwargs)
        return self.func(args,**kwargs)

