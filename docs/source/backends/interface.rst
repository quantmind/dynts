.. _interface:

===========================
Timeserie Interface
===========================


.. autoclass:: dynts.backends.base.tsbase
   :members:


.. _bckend-prop_func:

Proposed functionality
=========================
A timeseries should be able to get/set the value(s) for a given date. For example::

    >>> from dynts import timeseries
    >>> ts = timeseries('test')
    >>> dt = datetime.date(2010,01,01)
    >>> px = 101.1
    >>> ts[dt] = px
    >>> ts[dt]
    >>> 101.1

It should be able to perform standard mathematical functions on them as if they were vectors. For example::

    >>> ts2 = timeseries('test2')
    >>> ts2[dt] = 10.0
    >>> ts3 = ts1 + ts2
    >>> ts3
    >>> 2010-01-01 : 111.1

In the case where a date is missing from one of the series a suitable default/error value should be supplied::
    
    >>> dt2 = datetime.date(2010, 01, 02)
    >>> ts2[dt2] = 100.2
    >>> ts3 = ts2 + ts1
    >>> ts3
    >>> 2010-01-01 : 111.1
    ... 2010-01-02 : None
    
Potentially , each back-end will have its own ``missing value``, therefore a suitable conversion to a
unique ``python`` missing value needs to be in place.


In situations where access to the values is required by index (rather than by date) there is an appropriate helper class::

    >>> ts_as_matrix = as_matrix(ts3)
    >>> ts_as_matrix[0]
    >>> 111.1

This should be easy to do.


It may be useful to move functionality of the ts into a seperate 'analytics' object to avoid creating undue dependencies. Each function in the analytics object would return either a scalar value or another timeseries object with the same backend::

    >>> scalar_sd = ts.analytics.stdeviation(window = None)
    >>> ts_ma40 = ts.analytics.ma(window = 40)


    
