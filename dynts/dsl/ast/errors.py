
class ExpressionError(Exception):
    '''
    Expression Error
    '''
    
class CouldNotParse(ExpressionError):
    
    def __init__(self, f):
        msg = 'Failed to parse expression "%s"' % (f)
        super(CouldNotParse,self).__init__(msg)
    
class FunctionError(ExpressionError):
    '''Function Error'''
        
class FunctionInternalError(FunctionError):
    '''Function Error'''
    def __init__(self, function, msg):
        msg = 'Error in function "%s":' % (function,msg)
        super(FunctionInternalError,self).__init__(msg)
    
class FunctionDoesNotExist(FunctionError):
    '''
    Function does not exist
    '''
    def __init__(self, function):
        msg = 'Function "%s" does not exist' % function
        super(FunctionDoesNotExist,self).__init__(msg)
        
class FunctionTypeError(FunctionError):
    
    def __init__(self, function, msg):
        msg = 'Argument error in function "%s": %s' % (function,msg)
        super(FunctionTypeError,self).__init__(msg)
        
        
class BadConcatenation(ExpressionError):
    '''Error cause by bad concatentaiuon types'''
    def __init__(self, type1, type2):
        msg = 'Failed to concatenate %s with %s' % (type1,type2)
        super(BadConcatenation,self).__init__(msg)