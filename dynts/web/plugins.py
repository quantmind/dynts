'''Web plugins for djpcms
https://github.com/lsbardel/djpcms
'''
from djpcms import sites, plugins, forms, html
from djpcms.utils import markups
from djpcms.template import loader

from dynts import function_registry, function_title_and_body


class EconometricFunctions(plugins.DJPplugin):
    name = "econometric-functions"
    description = "Econometric Function"
    _docs = None
    
    def docs(self):
        try:
            rst = markups.get('rst')['handler']
        except:
            rst = lambda x : x
        if self._docs == None:
            data = []
            for name in sorted(function_registry):
                title,body = function_title_and_body(name)
                body = rst(body)
                data.append((name,title,body))
            self._docs = html.TextSelect(data,
                                         empty_label = '--------').render()
        return self._docs
    
    def render(self, djp, wrapper, prefix, **kwargs):
        return self.docs()

