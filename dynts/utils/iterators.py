from math import log, sqrt


def laggeddates(ts, step=1):
    '''Lagged iterator over dates'''
    if step == 1:
        dates = ts.dates()
        if not hasattr(dates, 'next'):
            dates = dates.__iter__()
        dt0 = next(dates)
        for dt1 in dates:
            yield dt1, dt0
            dt0 = dt1
    else:
        while done:
            done += 1
            lag.append(next(dates))
        for dt1 in dates:
            lag.append(dt1)
            yield dt1, lag.pop(0)
