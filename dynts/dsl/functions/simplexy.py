from dynts import xydata
from dynts.exceptions import FunctionTypeError, DateNotFound
from dynts.dsl import FunctionBase
from dynts.conf import settings


class SimpleFunctionXY(FunctionBase):
    abstract = True
    def __call__(self, args, **kwargs):
        return self.apply(args, **kwargs)
        

class scatter(SimpleFunctionXY):
    """\
A two-dimensional scatter for timeseries::

    scatter(GOOG,YHOO)
    
will create Google versus Yahoo prices withe date reference.
"""
    def apply(self, args, **kwargs):
        if not len(args) == 2:
            raise FunctionTypeError(self,"function requires two timeseries")
        ismissing = settings.ismissing
        ts0 = args[0]
        ts1 = args[1].ashash();
        name = '%s(%s,%s)' % (self.name,ts0.name,args[1].name)
        data = []
        for dt,v0 in ts0.items():
            try:
                v1 = ts1[dt]
            except DateNotFound:
                continue
            data.append((v0[0],v1[0],dt))
        return xydata(name = name, data = data,
                      lines = False,
                      extratype = 'date')
    
    