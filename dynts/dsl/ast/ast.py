from dynts.dsl.ast.binmath import *


class Function(Bracket):
    '''A time-serie function
    '''
    def __init__(self, func, expression, pl, pr):
        '''Create a function expression'''
        super(Function,self).__init__(expression, pl, pr)
        self.func = func
            
    def info(self):
        return '%s%s' % (self.func,super(Function,self).info())
    
    def _unwind(self, values, unwind, **kwargs):
        args   = []
        fargs = {'unwind_objects': unwind}
        arguments = self.value.unwind(values, unwind, sametype = False, full = True)
        if arguments.iterable():
            for a in arguments:
                self.functionarguments(a,args,fargs)
        else:
            self.functionarguments(arguments,args,fargs)
        
        args = tuple(args)
        try:
            result = self.func.unwind(*args,**fargs)
        except TypeError, e:
            msg = str(e).replace('apply() got an ','')
            raise FunctionTypeError(self.func, msg)
        except Exception, e:
            raise FunctionInternalError(self.func,e)
        result.label = str(self)
        return result
    
    def functionarguments(self, a, args, kwargs):
        d = a.internal_data()
        if isinstance(d,dict):
            kwargs.update(d)
        else:
            args.append(d)