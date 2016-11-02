from .registry import FunctionBase
from ...api.scatter import Scatter
from ...exc import FunctionTypeError, DateNotFound


class ScatterFunction(FunctionBase):
    """A two-dimensional scatter for timeseries::

        scatter(GOOG,YHOO)

    will create Google versus Yahoo prices withe date reference.
    """
    name = 'scatter'

    def __call__(self, args, **kwargs):
        if not len(args) == 2:
            raise FunctionTypeError(self, "function requires two timeseries")
        ts0 = args[0]
        ts1 = args[1].ashash();
        name = '%s(%s,%s)' % (self.name,ts0.name,args[1].name)
        data = []
        for dt, v0 in ts0.items():
            try:
                v1 = ts1[dt]
            except DateNotFound:
                continue
            data.append((v0[0], v1[0], dt))
        return Scatter(name=name, data=data, lines=False, extratype='date')
