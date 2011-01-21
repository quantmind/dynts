
class DyntsException(Exception):
    '''Base class of exceptions raised by ``dynts``'''
    pass

class InvalidBackEnd(DyntsException):
    '''A :class:`DyntsException` exception raised when
an invalid :class:`dynts.TimeSeries` bcakend name is given.'''
    pass

class MissingPackage(DyntsException):
    pass

class MissingDataProvider(DyntsException):
    '''A :class:`DyntsException` exception raised when
a Data provider is not available'''
    pass


class BadSymbol(DyntsException):
    '''A :class:`DyntsException` exception raised when
an exception occurs during parsing of a :class:`dynts.dsl.Symbol`'''
    pass


class FormattingException(DyntsException):
    '''A :class:`DyntsException` exception raised when
an exception occurs during formatting of a :class:`dynts.TimeSeries`'''
    pass


class DateNotFound(DyntsException):
    '''A :class:`DyntsException` exception raised when 
    a date is not found in a :class:`dynts.TimeSeries`.'''
    pass


class DyntsOutOfBound(DyntsException):
    '''A :class:`DyntsException` exception raised when 
    trying to access :class:`dynts.TimeSeries` outside its dates range.'''
    pass


class RightOutOfBound(DyntsOutOfBound):
    '''A :class:`DyntsOutOfBound` exception raised when 
    trying to access :class:`dynts.TimeSeries` after the end date.'''
    pass


class LeftOutOfBound(DyntsOutOfBound):
    '''A :class:`DyntsOutOfBound` exception raised when 
    trying to access :class:`dynts.TimeSeries` before the start date.'''
    pass


class ExpressionError(DyntsException):
    '''A :class:`DyntsException` exception raised when errors occur during
dsl language translation.
    '''

    
class CouldNotParse(ExpressionError):
    
    def __init__(self, f, data = None):
        msg = 'Failed to parse expression {0}: {1}'.format(f,data or '')
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
