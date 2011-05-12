'''Web plugins for djpcms
https://github.com/lsbardel/djpcms
'''
from djpcms import sites, forms
from djpcms.template import loader
from djpcms.plugins import DJPplugin


skin = getattr(sites.settings,'DYNTS_SKIN','dynts/ecoplot/skins/smooth.css')


class EcoForm(forms.Form):
    path = forms.CharField()
    default_show = forms.BooleanField(initial = True, required = False)
    height = forms.IntegerField()
    
    
class EcoPlot(DJPplugin):
    '''Plugin for djpcms__ content management system.

__ http://packages.python.org/djpcms/'''
    name = "econometric-plot"
    description = "Econometric plot"
    form = EcoForm
    template = 'dynts/econometric-plot.html'
    
    class Media:
        css = {
            'all': ('dynts/ecoplot/ecoplot.css', skin)
        }
        #js = ['dynts/flot/excanvas.min.js',
        #      'dynts/flot/jquery.flot.min.js',
        #      'dynts/flot/jquery.flot.selection.min.js',
        #      'dynts/jquery.flot.text.js',
        #      'dynts/ecoplot/ecoplot.js',
        #      'dynts/decorator.js']
        js = ['dynts/flot/excanvas.min.js',
              'dynts/flot/jquery.flot.js',
              'dynts/flot/jquery.flot.selection.js',
              'dynts/jquery.flot.text.js',
              'dynts/ecoplot/ecoplot.js',
              'dynts/decorator.js']
    
    def render(self, djp, wrapper, prefix, height = 400,
               default_show = True, path = '', start = None, **kwargs):
        height = abs(int(height))
        ctx = {'url':    path,
               'height': height,
               'default_show': default_show,
               'item':   djp.instancecode(),
               'start': start}
        return loader.render(self.template, ctx)
    

class EconometricFunctions(DJPplugin):
    name = "econometric-functions"
    description = "Econometric Function"
    
    def render(self, djp, wrapper, prefix, **kwargs):
        ops = operators.all()
        rops = []
        for op in ops.values():
            rops.append({'operator': op.__name__,
                         'fullname': op.fullname,
                         'description': op.__doc__})
        return loader.render_to_string('instdata/operators.html', {'items': rops})

