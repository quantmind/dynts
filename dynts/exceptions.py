
class DyntsException(Exception):
    '''Base class of exceptions raised by ``dynts``'''
    pass

class InavlidBackEnd(DyntsException):
    pass

class MissingPackage(DyntsException):
    pass

class MissingDataProvider(DyntsException):
    '''A :class:`DyntsException` exception raised when
a Data provider is not available'''
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