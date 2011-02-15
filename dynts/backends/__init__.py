from dynts.utils import import_module
from dynts.conf import settings

from .xy import *
from .base import TimeSeries, ops, ts_bin_op

BACKENDS = {
    'zoo': 'zoo',
    'numpy': 'tsnumpy',
}

istimeseries = lambda value : isinstance(value,TimeSeries)
isxy = lambda value : isinstance(value,xydata)


def timeseries(name = '', backend = None, **kwargs):
    '''Create a new :class:`dynts.TimeSeries` object.'''
    from dynts import InvalidBackEnd
    backend = backend or settings.backend
    bname = BACKENDS.get(backend,None)
    if bname:
        bmodule = 'dynts.backends.%s' % bname
    else:
        bmodule = backend
    module = import_module(bmodule)
    name = name or bmodule
    try:
        factory = getattr(module, 'TimeSeries')
    except AttributeError:
        raise InvalidBackEnd('Could not find a TimeSeries class in module %s' % bmodule)
    return factory(name = name, **kwargs)
