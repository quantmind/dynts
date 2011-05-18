'''Web views for djpcms 
https://github.com/lsbardel/djpcms
'''
from djpcms import views, forms
from djpcms.html import HtmlWidget
from djpcms.utils import gen_unique_id

from ccy import dateFromString


class EcoForm(forms.Form):
    height = forms.IntegerField()
    

class TimeSeriesView(views.ModelView):
    '''``djpcms`` application view for retriving timeseries data as  JSON string.
Available as Ajax Get response.'''
    plugin_form = EcoForm
    _methods      = ('get',)
    
    def render(self, djp):
        kwargs = djp.kwargs
        height = max(int(kwargs.get('height',400)),30)
        start = kwargs.get('start',None)
        code = self.get_code_object(djp)
        id = gen_unique_id()
        widget = HtmlWidget('div', id = id, cn = 'econometric-plot')
        widget.addData('height',height)\
              .addData('item',code)\
              .addData('start',start)\
              .addData('url',self.path)
        return widget.render()
    
    def ajax_get_response(self, djp):
        request = djp.request
        return self.econometric_data(djp.request, dict(request.GET.items()))
    
    def get_code_object(self, djp):
        '''Check if the code is an instance of a model.'''
        return None
           
    def econometric_data(self, request, data):
        #Obtain the data
        cts    = data.get('command',None)
        start  = data.get('start',None)
        end    = data.get('end',None)
        period = data.get('period',None)
        #object = self.get_object(cts)
        #if object:
        #    cts = self.codeobject(object)
        if start:
            start = dateFromString(str(start))
        if end:
            end = dateFromString(str(end))
        return self.getdata(request,cts,start,end)
    
    def getdata(self,request,expression,start,end):
        '''Pure virtual function which retrives the actual data.
It must return a JSON string.'''
        raise NotImplementedError
    
        class Media:
            js = ['dynts/flot/excanvas.min.js',
                  'dynts/flot/jquery.flot.js',
                  'dynts/flot/jquery.flot.selection.js',
                  'dynts/jquery.flot.text.js',
                  'dynts/ecoplot/ecoplot.js',
                  'dynts/decorator.js']
    