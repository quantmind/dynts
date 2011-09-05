'''Web plugins for djpcms
https://github.com/lsbardel/djpcms
'''
from djpcms import sites, plugins, forms, html, memoized
from djpcms.utils import markups
from djpcms.template import loader

from dynts import function_registry, function_title_and_body


@memoized
def docs():
    try:
        rst = markups.get('rst')['handler']
    except:
        rst = lambda x : x
    choices = [('','-----------')]
    text = []
    for name in sorted(function_registry):
        title,body = function_title_and_body(name)
        body = rst(body)
        choices.append((name,title))
        text.append((name,body))
    return html.TextSelect(choices,text)


class EconometricFunctions(plugins.DJPplugin):
    name = "econometric-functions"
    description = "Econometric Function"
    
    def render(self, djp, wrapper, prefix, **kwargs):
        return docs()

