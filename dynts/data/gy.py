import os
import csv

try:
    from urllib2 import urlopen, ProxyHandler, build_opener
except ImportError:
    from urllib.request import urlopen, ProxyHandler, build_opener
    
try:
    import httplib2
except:
    httplib2 = None

from dynts.conf import settings

from .base import DataProvider


short_month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')


class WebCsv(DataProvider):

    def __init__(self):
        if httplib2:
            self.h = httplib2.Http()
        else:
            self.h = None
        self.h = None
        
    @property
    def http(self):
        proxy = ProxyHandler(settings.proxies)
        return build_opener(proxy)
        
    def string_to_date(self, sdte):
        from ccy import dateFromString
        return dateFromString(sdte)
    
    def request(self, url):
        if self.h:
            resp, content = self.h.request(url)
            if resp.status == 200:
                return resp
        else:
            return self.http.open(url)
    
    def rowdata(self, ticker, startdate, enddate):
        url = self.hystory_url(str(ticker), startdate, enddate)
        res = self.request(url)
        return csv.DictReader(res)
        
    def hystory_url(self, ticker, startdate, enddate, field = None):
        raise NotImplementedError
    
    def allfields(self, ticker = None):
        return ['Close','Open','Low','High','Volume']
        
    def load(self, symbol, startdate, enddate, logger, backend, **kwargs):
        ticker = symbol.ticker
        field  = symbol.field
        data = self.rowdata(ticker, startdate, enddate)
        if not data:
            return

        fields = {}        
        std  = self.string_to_date
        datestr = None
        dates = []
        for r in data:
            try:
                if not datestr:
                    val   = None
                    dt    = None
                    found = 0
                    for k,v in r.items():
                        if len(k) >= 4:
                            if k[len(k)-4:] == 'Date':
                                datestr = k
                                continue
                        fields[str(k).upper()] = []
                
                dt  = std(r[datestr])
                dates.append(dt)
                for k,v in r.items():
                    nts = fields.get(str(k).upper(),None)
                    if nts is not None:
                        try:
                            nts.append(float(v))
                        except:
                            continue
            except:
                continue
        
        field = field or 'CLOSE'
        return {'date': dates,
                'value': fields.get(str(field).upper(),None)}


class google(WebCsv):
    baseurl = 'http://finance.google.com/finance'
        
    def getdate(self, st, dte):
        m = short_month[dte.month-1]
        return '%s=%s+%s,+%s' % (st,m,dte.day,dte.year)
        
    def hystory_url(self, ticker, startdate, enddate, field = None):
        b = self.baseurl
        st = self.getdate('startdate', startdate)
        et = self.getdate('enddate', enddate)
        return '%s/historical?q=%s&%s&%s&output=csv' % (b,ticker,st,et)
    
    def weblink(self, ticker):
        return '%s?q=%s' % (self.baseurl,ticker)
    

class yahoo(WebCsv):
    baseurl = 'http://ichart.yahoo.com'
        
    def getdate(self, st, dte):
        return '%s=%s&%s=%s&%s=%s' % (st[0],dte.month-1,st[1],dte.day,st[2],dte.year)
        
    def hystory_url(self, ticker, startdate, enddate):
        b = self.baseurl
        st = self.getdate(('a','b','c'), startdate)
        et = self.getdate(('d','e','f'), enddate)
        return '%s/table.csv?s=%s&%s&%s&g=d&ignore=.csv' % (b,ticker,st,et)
    
    def weblink(self, ticker):
        return 'http://finance.yahoo.com/q?s=%s' % ticker


