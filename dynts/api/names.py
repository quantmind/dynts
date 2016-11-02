from functools import reduce

from ..conf import settings


def tsname(*names):
    sp = settings.splittingnames
    return reduce(lambda x, y: '%s%s%s' % (x, sp, y), names)


def composename(name, *names, **kwargs):
    sp = settings.splittingnames
    kw = ','.join(('{0}={1}'.format(*v) for v in kwargs.items()))
    if kw:
        kw = ',' + kw
    return sp.join(('{0}({1}{2})'.format(name, x, kw) for x in names))
