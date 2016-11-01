cdef int _EPOCH_ORD = 719163

cdef extern from "datetime.h":
    
    ctypedef class datetime.date [object PyDateTime_Date]:
        # cdef int *data
        # cdef long hashcode
        # cdef char hastzinfo
        pass
    
    ctypedef class datetime.datetime [object PyDateTime_DateTime]:
        # cdef int *data
        # cdef long hashcode
        # cdef char hastzinfo
        pass

    int PyDateTime_GET_YEAR(datetime o)
    int PyDateTime_GET_MONTH(datetime o)
    int PyDateTime_GET_DAY(datetime o)
    int PyDateTime_DATE_GET_HOUR(datetime o)
    int PyDateTime_DATE_GET_MINUTE(datetime o)
    int PyDateTime_DATE_GET_SECOND(datetime o)
    int PyDateTime_DATE_GET_MICROSECOND(datetime o)
    int PyDateTime_TIME_GET_HOUR(datetime o)
    int PyDateTime_TIME_GET_MINUTE(datetime o)
    int PyDateTime_TIME_GET_SECOND(datetime o)
    int PyDateTime_TIME_GET_MICROSECOND(datetime o)
    bint PyDateTime_Check(object o)
    void PyDateTime_IMPORT()

# import datetime C API
PyDateTime_IMPORT


cdef inline int64_t jstimestamp(object dt):
    '''Convert a python date to a unix timestamp'''
    cdef int y, m, d, h, mn, s, ms, days

    y = PyDateTime_GET_YEAR(dt)
    m = PyDateTime_GET_MONTH(dt)
    d = PyDateTime_GET_DAY(dt)

    hours = 24 * (date(y, m, 1).toordinal() - _EPOCH_ORD + d - 1)
    
    if isinstance(dt,datetime.date):
        ts = 3600000 * hours
    else:
        hours += PyDateTime_DATE_GET_HOUR(dt)
        mn = PyDateTime_DATE_GET_MINUTE(dt)
        s = PyDateTime_DATE_GET_SECOND(dt)
        ms = PyDateTime_DATE_GET_MICROSECOND(dt) / 1000
        ts = 1000*((hours * 60 + mn) * 60 + s) + ms
        
    return <int64_t>(ts)
