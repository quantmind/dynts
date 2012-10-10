from dynts.utils import import_module
from dynts.conf import settings

from .xy import *
from .base import *

BACKENDS = {
    'zoo': 'zoo',
    'numpy': 'tsnumpy',
}

__all__ = ['timeseries','istimeseries','isxy']

istimeseries = lambda value : isinstance(value,TimeSeries)
isxy = lambda value : isinstance(value,xydata)


def timeseries(name='', backend=None, date=None, data=None, **kwargs):
    '''Create a new :class:`dynts.TimeSeries` instance using a given *backend*
and populating it with provided the data.

:parameter name: optional timeseries name. For multivarate timeseries
                 the :func:`dynts.tsname` utility function can be used
                 to build it.
:parameter backend: optional backend name. If not provided, numpy will be used.
:parameter date: optional iterable over dates.
:parameter data: optional iterable over data.
'''
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
        raise InvalidBackEnd(
                'Could not find a TimeSeries class in module %s' % bmodule)
    return factory(name = name, date = date, data = data, **kwargs)
