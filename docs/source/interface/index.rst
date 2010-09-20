.. _interface:

===========================
Timeserie Interface
===========================

To create a :class:`dynts.TimeSeries` object directly you need the
:func:`dynts.timeseries` function:

.. autofunction:: dynts.timeseries

For example::

    >>> from dynts import timeseries
    >>> ts = timeseries('test')
    >>> t
    TimeSeries:zoo:test

Lets get a timeserie with some data::

	>>> import dynts
	>>> from datetime import date
	>>> ts = dynts.evaluate('GOOG').unwind()
	>>> ts
	TimeSeries:zoo:GOOG
	>>> ts.count()
	1
	>>> len(ts)
	251
	>>> b = ts.asbtree()
	>>> b[date(2010,9,15)]
	480.634
	


.. toctree::
   :maxdepth: 2

   interface
   design
