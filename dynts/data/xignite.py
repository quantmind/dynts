
class XigniteProxy(object):
    baseurl  = 'http://www.xignite.com/'
    products = {'ccy':'',
                'rates':'xRates.asmx'}

    
class xignite(DataProvider):
    proxy   = XigniteProxy()
    baseurl = 'http://www.xignite.com/xCurrencies.asmx/'
        
    