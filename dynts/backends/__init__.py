from dynts.utils.importlib import import_module
from dynts.conf import settings
from base import tsbase

BACKENDS = {
    'zoo': 'zoo',
    'rmetrics': 'rmetrics'
}

istimeserie = lambda value : isinstance(value,tsbase)

def timeserie(name = '', backend = None, **kwargs):
    '''Create a new timeserie object.'''
    backend = backend or settings.backend
    bname = BACKENDS.get(backend,None)
    if bname:
        bmodule = 'dynts.backends.%s' % bname
    else:
        bmodule = backend
    module = import_module(bmodule)
    name = name or bmodule
    return getattr(module, 'timeserie')(backend, name = name, **kwargs)