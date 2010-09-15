

toupper = lambda x : str(x).upper()

class Settings(object):
    '''The setting class contains configuration parameters used in dynts. To change settings::
    
    from dynts.conf import settings
    
    settings.default_provider = 'google'
    '''
    def __init__(self):
        self.backend = 'zoo'
        self.concat_operator    = ','
        self.separator_operator = '|'
        self.default_provider   = 'yahoo'
        self.months_history     = 12
        self.proxies = {}
        self.symboltransform = toupper
        
    @property
    def special_operators(self):
        return [self.concat_operator,self.separator_operator]
    
        
        
settings = Settings()
