
class DyntsException(Exception):
    pass

class MissingPackage(DyntsException):
    pass

class MissingDataProvider(DyntsException):
    '''Data provider is not available'''
    pass