'''Web plugins for djpcms
https://github.com/lsbardel/djpcms
'''
from djpcms import plugins, forms, html
from djpcms.utils import markups

from dynts import function_registry, function_title_and_body


def docs(request):
    try:
        rst = markups.get('rst')['handler']
    except:
        rst = lambda x : x
    choices = [('','-----------')]
    text = []
    for name in sorted(function_registry):
        title,body = function_title_and_body(name)
        body = rst(request, body)
        yield name,title,body


class EconometricFunctions(plugins.DJPplugin):
    name = "econometric-functions"
    description = "Econometric Function"
    
    def render(self, request, wrapper, prefix, **kwargs):
        name_title_body = docs(request)
        return html.ajax_html_select(name_title_body).render(request)

