from djpcms import views
from djpcms import html
from djpcms.template import loader

import medplate

from dynts.web.views import TimeSeriesView, TimeSeriesAppMixin
from dynts.web.plugins import docs


def context_process(request):
    if not request.is_xhr:
        style = request.REQUEST.get('style','smooth')
        return {'style':style}



def tabview(djp):
    make = lambda d,kwargs : djp.view.get_widget(d).addData('height',500)\
                                     .addData(kwargs).render(d)
    anchor = lambda s : html.Widget('a',title=s,href='/?style={0}'.format(s))\
                            .render(inner = s)
    data = (('default',make(djp,None)),
            ('popup',make(djp,{'edit':{'popup':True}})),
            #('resizable',make(djp,{'resizable':{'disabled':False}}))
            )
    tabs = html.tabs(data_stream = data,
                     cn = 'whole-page')
    styles = html.Box(hd = 'Styles',
                      bd = html.List((anchor(s) for s in medplate.themes()),
                                     cn = 'vertical').render(djp))
    logging = html.Box(hd = 'Logging',
                       bd = html.Widget('div',cn='djp-logging-panel').render())
    
    ctx = {'content0':views.BlockContentGen(djp,(tabs,)),
           'content1':views.BlockContentGen(djp,(styles,docs(),logging))}
    
    return loader.render('djpcms/inner/cols2_66_33.html',
                         loader.context(ctx,djp.request))


class Application(TimeSeriesAppMixin,views.Application):
    view = TimeSeriesView(renderer = tabview)
    