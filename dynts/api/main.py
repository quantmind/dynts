from ..conf import settings
from ..exc import InvalidBackEnd
from ..utils.populate import datepopulate, populate
from .timeseries import BACKENDS


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
    TS = BACKENDS.get(backend)
    if not TS:
        raise InvalidBackEnd(
            'Could not find a TimeSeries class %s' % backend
        )
    return TS(name=name, date=date, data=data, **kwargs)


def randomts(size=100, cols=1, start=None, delta=1,
             generator=None, backend=None, name='randomts'):
    dates = datepopulate(size, start=start, delta=delta)
    data = populate(size, cols=cols, generator=generator)
    return timeseries(name=name, backend=backend, date=dates, data=data)
