import numpy as np
cimport numpy as np
cimport cython
from numpy cimport *

cdef extern from "numpy/arrayobject.h":
    void import_array()

cdef extern from "math.h":
    double log(double x)
    double sqrt(double x)

# Not a number
isnan = np.isnan
cdef double NaN = <double> np.NaN
cdef double clog2 = log(2.)

# initialize numpy
import_array()

cdef inline int int_max(int a, int b): return a if a >= b else b
cdef inline int int_min(int a, int b): return a if a >= b else b

# MSVC does not have log2!
cdef inline double Log2(double x):
    return log(x) / clog2

cdef extern from "datetime.h":

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
