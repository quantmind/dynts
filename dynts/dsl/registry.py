import inspect
from UserDict import UserDict


class FunctionRegistry(UserDict):
    
    def __init__(self):
        self.data = {}
        
    def register(self, function):
        """Register a function in the function registry.
        The function will be automatically instantiated if not already an
        instance.
        """
        function = inspect.isclass(function) and function() or function
        name = function.name
        self.data[name] = function

    def unregister(self, name):
        """Unregister function by name.
        """
        try:
            name = name.name
        except AttributeError:
            pass
        return self.pop(name,None)


class ASTFunctionMeta(type):
    '''Meta class magic'''    
    def __new__(cls, name, bases, attrs):
        global function_registry
        super_new = super(ASTFunctionMeta, cls).__new__

        # Abstract class, remove the abstract attribute so
        # any class inheriting from this won't be abstract by default.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return super_new(cls, name, bases, attrs)

        # Automatically generate missing name.
        function_name = attrs.get("name",None) or name
        function_name = function_name.lower()
        attrs["name"] = function_name
        if function_name not in function_registry:
            function_cls = super_new(cls, name, bases, attrs)
            function_registry.register(function_cls)
        return function_registry[function_name].__class__
    
    
class FunctionBase(object):
    '''Base class for a timeseries function implementation.
The only member function to implement is the ``__call__`` method.

    .. function:: __call__(args, **kwargs)
        
        where *args* is a list of arguments (timeseries or other objects) and
        *kwargs* is a dictionary of input parameters.
        For example, the rolling-standard deviation is defined as::
            
            std(expression,window=20)
    '''
    __metaclass__ = ASTFunctionMeta
    abstract = True
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

function_registry = FunctionRegistry()


