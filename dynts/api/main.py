from importlib import import_module

from ..conf import settings
from ..exc import InvalidBackEnd


def timeseries(name='', backend=None, date=None, data=None, **kwargs):
    '''Create a new :class:`dynts.TimeSeries` instance using a ``backend``
    and populating it with provided the data.

    :parameter name: optional timeseries name. For multivarate timeseries
                     the :func:`dynts.tsname` utility function can be used
                     to build it.
    :parameter backend: optional backend name.
        If not provided, numpy will be used.
    :parameter date: optional iterable over dates.
    :parameter data: optional iterable over data.
    '''
    backend = backend or settings.backend
    bname = BACKENDS.get(backend, None)
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
