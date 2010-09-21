

class DataProvider(object):
    '''Interface class for Data Providers'''
        
    def __repr__(self):
        return self.code + ' financial data provider'
    
    def get(self, ticker, startdate, enddate, field = None):
        '''This is the function to implemenet.
        '''
        raise NotImplementedError
    
    def isconnected(self):
        '''Return ``True`` if data connection is available
        '''
        return True
    
    def __get_code(self):
        return self.__class__.__name__
    code = property(fget = __get_code)
    
    def weblink(self, ticker):
        '''Optional web link for a given *ticker*. Default return ``None``.
        '''
        return None
    
    def external(self):
        return True
    
    def hasfeed(self, live = False):
        return not live
    
    def connect(self):
        pass
    

