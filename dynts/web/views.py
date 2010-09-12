from django import http
from djpcms.views import appview

from dateutil.parser import parse as DateFromString

def date2yyyymmdd(dte):
    return dte.day + 100*(dte.month + 100*dte.year)

class TimeserieView(appview.AppView):
    '''View used to obtain timeseries.
The only view available is an Ajax Get view.'''
    _methods      = ('get',)
    
    def get_response(self, djp):
        request = djp.request
        if not request.is_ajax():
            raise http.Http404
        sdata = self.econometric_data(dict(request.GET.items()))
        return http.HttpResponse(sdata, mimetype='application/javascript')
    
    def get_object(self, code):
        '''Check if the code is an instance of a model.'''
        codes = code.split(':')
        if len(codes) == 2 and codes[0] == str(self.model._meta):
            try:
                return self.model.objects.get(id = int(codes[1]))
            except:
                return None
                
    def econometric_data(self, data):
        proxy  = self.get_proxy()
        cts    = data.get('command',None)
        start  = data.get('start',None)
        end    = data.get('end',None)
        period = data.get('period',None)
        object = self.get_object(cts)
        if object:
            cts = self.codeobject(object)
        if start:
            start = date2yyyymmdd(DateFromString(str(start)).date())
        if end:
            end = date2yyyymmdd(DateFromString(str(end)).date())
        try:
            return proxy.get(cts,start,end)
        except IOError, e:
            return ''
    
    def codeobject(self, object):
        return str(object)
    
    def get_proxy(self):
        return self
    
    