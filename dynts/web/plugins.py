from django.conf import settings
from django import forms
from django.template import loader

from djpcms.utils import mark_safe
from djpcms.plugins import DJPplugin
from djpcms.views import appsite

skin = getattr(settings,'DYNTS_SKIN','dynts/ecoplot/skins/smooth.css')


class EcoForm(forms.Form):
    url    = forms.CharField()
    height = forms.IntegerField()
    
class EcoPlot(DJPplugin):
    '''Plugin for djpcms__ content management system.

__ http://packages.python.org/djpcms/'''
    name = "econometric-plot"
    description = "Econometric plot"
    form = EcoForm
    
    class Media:
        css = {
            'all': ('dynts/ecoplot/ecoplot.css', skin)
        }
        js = ['dynts/flot/excanvas.min.js',
              'dynts/flot/jquery.flot.js',
              'dynts/ecoplot/ecoplot.js',
              'dynts/decorator.js']
    
    def render(self, djp, wrapper, prefix, height = 400, url = '', **kwargs):
        height = abs(int(height))
        ctx = {'url':    url,
               'height': height,
               'item':   djp.instancecode()}
        return loader.render_to_string('dynts/econometric-plot.html', ctx)
    

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

