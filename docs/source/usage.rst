
============================
Usage
============================


Create
=====================

To create a :class:`dynts.TimeSeries` object directly you need the
:func:`dynts.timeseries` function:

For example::

    >>> from dynts import timeseries
    >>> ts = timeseries('test')
    >>> t
    TimeSeries:numpy:test
    >>> ts.type
    'numpy'
    >>> ts.shape
    (0,0)
    
By default, timeseries used numpy_ as their back-end data structure.
Other backends are available and custom back-ends can also be used as
explained in :ref:`timeseries backends <backends>`.

Lets get a timeserie with some data. In this example we study
Google and its 20 days moving avarage::

	>>> import dynts
	>>> from datetime import date
	>>> ts = dynts.evaluate('goog,ma(goog,window=20)').ts()
	>>> ts
	TimeSeries:numpy:GOOG__ma(GOOG,window=20)
	>>> ts.names()
	['GOOG', 'ma(GOOG,window=20)']
	>>> ts.count()
	2
	>>> len(ts)
	251
	>>> b = ts.asbtree()
	>>> b[date(2010,9,15)]
	480.634
	
You can also use standard matrix slicing and indexing on data:

    >>> ts[0]
    array([ 484.78,    nan])
    >>> ts[-1]
    array([ 519.03,  525.894])
    >>> ts[-4:]
    
and so forth.


.. _merging:

Merging TimeSeries
===========================

To merge an iterable over timeseries::

	import dynts
	ts = dynts.merge(tseries)


.. _rolling-function:

Rolling functions
============================

A rolling function is a generic term for applying a function to rolling margins of a
:class:`dynts.TimeSeries`.


.. _numpy: http://numpy.scipy.org/