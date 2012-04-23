from djpcms import views, forms, html
from djpcms.utils import gen_unique_id, media

import dynts
from ccy import dateFromString

from .html import FLOT_MEDIA


class EcoForm(forms.Form):
    height = forms.IntegerField()
    service_url = forms.CharField(required = False)
    method = forms.ChoiceField(choices = (('get','get'),('post','post')),
                               default = 'get')
    windows = forms.CharField(\
            required = False,
            help_text='Comma separated list of time windows (e.g. 3y,2y,1y,6m)')
    
    
class PlotSettings(forms.Form):
    line_fill = forms.BooleanField()
    bar_fill = forms.BooleanField()
    
    
class TimeSeriesAppMixin(object):
    
    def get_code_object(self, request):
        return None
    
    def getdata(self, request, expression, start, end, **kwargs):
        res = dynts.evaluate(expression, start = start, end = end)
        return res.dump('flot')
    

class TimeSeriesView(views.ModelView):
    '''``djpcms`` application view for retrieving time-series data as object.
It renders as an econometric plot jQuery plugin and it has an AJAX get response
for fetching data.'''
    has_plugins = True
    plugin_form = EcoForm
    description = 'Timeseries and Scatter Plots'
    flot_media = FLOT_MEDIA
    _methods = ('get',)
    
    def get_widget(self, request, height=400, service_url = None,
                   method = 'get', windows=None, start = None, **kwargs):
        service_url = service_url or self.path
        code = self.get_code_object(request)
        id = gen_unique_id()
        if windows:
            windows = [w.replace(' ','') for w in windows.split(',')]
        widget = html.Widget('div', id = id, cn = 'econometric-plot')\
                .addData('height',height)\
                .addData('start',start)\
                .addData('windows',{'windows':windows})\
                .addData('jsondata',{'url':service_url,
                                     'requestMethod':method})
        if code:
            widget.addData('command',{'show':False,'symbol':code})
        return widget
            
    def render(self, request, **kwargs):
        return self.get_widget(request, **kwargs).render(request)
    
    def get_code_object(self, request):
        return self.appmodel.get_code_object(request)
    
    def ajax_get_response(self, request):
        return self.econometric_data(request, dict(request.GET.items()))
           
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
        return self.appmodel.getdata(request,cts,start,end)
    
    def media(self, request):
        return self.flot_media
    
