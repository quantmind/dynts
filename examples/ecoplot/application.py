from djpcms import views
from djpcms import html
import medplate

from dynts.web.views import TimeSeriesView, TimeSeriesAppMixin


def context_process(request):
    if not request.is_xhr:
        style = request.REQUEST.get('style','smooth')
        return {'style':style,
                'styles':medplate.themes()}



def tabview(djp):
    make = lambda d,kwargs : djp.view.get_widget(d).addData(kwargs).render(d)
    data = (('default',make(djp,None)),
            ('popup',make(djp,{'edit':{'popup':True}})),
            #('resizable',make(djp,{'resizable':{'disabled':False}}))
            )
    return html.tabs(data_stream = data,
                     cn = 'whole-page').render(djp)
    


class Application(TimeSeriesAppMixin,views.Application):
    view = TimeSeriesView(renderer = tabview)
    