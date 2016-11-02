from ..conf import settings
from .. import lib


def rollsingle(self, func, window=20, name=None, fallback=False,
               align='right', **kwargs):
    '''Efficient rolling window calculation for min, max type functions
    '''
    rname = 'roll_{0}'.format(func)
    if fallback:
        rfunc = getattr(lib.fallback, rname)
    else:
        rfunc = getattr(lib, rname, None)
        if not rfunc:
            rfunc = getattr(lib.fallback, rname)
    rolling = lambda serie : list(rfunc(serie,window))
    data = np.array([rolling(serie) for serie in self.series()])
    name = name or self.makename(func,window=window)
    dates = asarray(self.dates())
    desc = settings.desc
    if (align == 'right' and not desc) or desc:
        dates = dates[window-1:]
    else:
        dates = dates[:-window+1]
    return self.clone(dates, data.transpose(), name = name)
