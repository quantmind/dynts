'''Web plugins for djpcms
https://github.com/lsbardel/djpcms
'''
from djpcms import sites, plugins
from djpcms.template import loader


class EconometricFunctions(plugins.DJPplugin):
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

