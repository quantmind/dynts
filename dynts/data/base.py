
class DataProvider(object):
    '''Interface class for Data Providers'''
        
    def __repr__(self):
        return self.code + ' financial data provider'
    
    def __get_code(self):
        return self.__class__.__name__
    code = property(fget = __get_code)
    
    def weblink(self, ticker):
        '''
        Provide a link to a web page
        '''
        return None
    
    def external(self):
        return True
    
    def hasfeed(self, live = False):
        return not live
    
    def connect(self):
        pass
        
    def isconnected(self):
        '''
        Return True if data vendor connection is available
        '''
        return True
    
    def get(self, ticker, startdate, enddate, field = None):
        '''
        this function should be implemeneted by derived classes.
        By default do nothing, which is fine
        '''
        raise NotImplementedError
    

