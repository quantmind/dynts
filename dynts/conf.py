from math import isnan
toupper = lambda x : str(x).upper()

class Settings(object):
    '''The setting class contains configuration parameters used in dynts.
    
    .. attribute:: backend
    
        the default :class:`dynts.TimeSeries` backend class, Default ``zoo``.
        
    .. attribute:: concat_operator
    
        The operator for concatenating expressions. Default ``,``.
    
    .. attribute:: default_loader
    
        Default :class:`dynts.data.TimeSerieLoader` class. Default ``None``.
        If this is ``None`` the :class:`dynts.data.TimeSerieLoader` class will be used as loder.
        
    .. attribute:: default_provider
    
        Default :class:`dynts.data.DataProvider` code. Default ``"YAHOO"``.
        
    .. attribute:: field_separator
    
        Character used to separate tickers from fields and providers. Default ``:``.
        
    .. attribute:: months_history
    
        the default number of months of history. Default: ``12``.
        
    .. attribute:: proxies
    
        dictionary of proxy servers. Default ``{}``.
        If you need to use a proxy server to access the web::
        
            from dynts.conf import settings
            settings.proxies['http'] = 'http://yourproxy.com:80'
                
To change settings::
    
    from dynts.conf import settings
    
    settings.default_provider = 'GOOGLE'
    '''
    def __init__(self):
        self.backend = 'zoo'
        self.splittingnames     = '__'
        self.concat_operator    = ','
        self.separator_operator = '|'
        self.default_provider   = 'YAHOO'
        self.field_separator    = ':'
        self.idregex = '[a-zA-Z_][a-zA-Z_0-9:@]*'
        self.default_loader     = None
        self.months_history     = 12
        self.proxies = {}
        self.symboltransform = toupper
        self.default_daycounter = 'ACT/365'
        self.missing_value      = float('nan')
        
    @property
    def special_operators(self):
        return [self.concat_operator,self.separator_operator]
    
    def getdc(self):
        import ccy
        return ccy.getdc(self.default_daycounter)
    
    def ismissing(self, value):
        return isnan(value)
    
        
        
settings = Settings()
