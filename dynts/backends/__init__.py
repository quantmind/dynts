from dynts.utils.importlib import import_module
from dynts.conf import settings
from base import TimeSeries

BACKENDS = {
    'zoo': 'zoo',
    'rmetrics': 'rmetrics'
}

istimeseries = lambda value : isinstance(value,TimeSeries)

def timeseries(name = '', backend = None, **kwargs):
    '''Create a new :class:`dynts.TimeSeries' object.'''
    backend = backend or settings.backend
    bname = BACKENDS.get(backend,None)
    if bname:
        bmodule = 'dynts.backends.%s' % bname
    else:
        bmodule = backend
    module = import_module(bmodule)
    name = name or bmodule
    return getattr(module, 'timeserie')(name = name, **kwargs)