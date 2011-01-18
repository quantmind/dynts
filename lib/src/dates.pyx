cdef int _EPOCH_ORD = 719163

from datetime import date, datetime


cdef inline int64_t jstimestamp(object dt):
    '''Convert a python date to a unix timestamp'''
    cdef int y, m, d, h, mn, s, ms, days

    y = PyDateTime_GET_YEAR(dt)
    m = PyDateTime_GET_MONTH(dt)
    d = PyDateTime_GET_DAY(dt)

    hours = 24 * (date(y, m, 1).toordinal() - _EPOCH_ORD + d - 1)
    
    if isinstance(dt,date):
        ts = 3600000 * hours
    else:
        hours += PyDateTime_DATE_GET_HOUR(dt)
        mn = PyDateTime_DATE_GET_MINUTE(dt)
        s = PyDateTime_DATE_GET_SECOND(dt)
        ms = PyDateTime_DATE_GET_MICROSECOND(dt) / 1000
        ts = 1000*((hours * 60 + mn) * 60 + s) + ms
        
    return <int64_t>(ts)