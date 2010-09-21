.. _index-main:

=================================
DynTS
=================================

.. rubric:: A domain specific language for Timeseries_ analysis and manipulation.

**Get it**
:ref:`Overview, Installation and Development <intro-overview>`

**What is it?**
Assuming you are familiar with timeseries, this is the idea::

	>>> import dynts
	>>> ts1 = dynts.evaluate('GOOG')
	>>> # evaluate rolling annualised volatility on a 30 days windows
	... ts2 = dynts.evaluate('avol(GOOG,window=30)')
	>>> # specify start and end date
	... ts3 = dynts.evaluate('avol(GOOG,window=30)', start = date(2007,1,1), end = date(2010,1,1))
	
**Where does it get the data?**
Pluggable :class:`dynts.data.DataProvider`.

**How econometric calculations are performed?** Extendible :class:`dynts.TimeSeries` backend classes.

Dynts is in constant development, with new functionalities added on a daily basis.

Contents						
==================

.. toctree::
   :maxdepth: 1
   
   interface/index
   dsl/index
   backends/index
   provider/index
   formatters
   internals/index
   web/index

	
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Timeseries: http://en.wikipedia.org/wiki/Time_series
