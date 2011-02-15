'''Web views for djpcms 
https://github.com/lsbardel/djpcms
'''
from djpcms.views import appview

from ccy import dateFromString


class TimeSeriesView(appview.ModelView):
    '''```djpcms``` application view for retriving timeseries data as  JSON string.
Available as Ajax Get response.'''
    _methods      = ('get',)
    
    def ajax_get_response(self, djp):
        request = djp.request
        sdata = self.econometric_data(djp.request, dict(request.GET.items()))
        return djp.http.HttpResponse(sdata, mimetype='application/javascript')
    
    def get_object(self, code):
        '''Check if the code is an instance of a model.'''
        codes = code.split(':')
        if len(codes) == 2 and codes[0] == str(self.model._meta):
            try:
                return self.model.objects.get(id = int(codes[1]))
            except:
                return None
                
    def econometric_data(self, request, data):
        #Obtain the data
        cts    = data.get('command',None)
        start  = data.get('start',None)
        end    = data.get('end',None)
        period = data.get('period',None)
        object = self.get_object(cts)
        if object:
            cts = self.codeobject(object)
        if start:
            start = dateFromString(str(start))
        if end:
            end = dateFromString(str(end))
        try:
            return self.getdata(request,cts,start,end)
        except IOError, e:
            return ''
    
    def codeobject(self, object):
        return str(object)
    
    def getdata(self,request,expression,start,end):
        '''Pure virtual function which retrives the actual data.
It must return a JSON string.'''
        raise NotImplementedError
    
    