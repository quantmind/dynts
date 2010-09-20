.. _data-loader:

===========================
Data Loader
===========================

This section deals with loading data from data providers.
Data providers are used to populate :class:`dynts.dsl.Symbol`
instances with actual data. For example::

	>>> import dynts
	>>> ts = dynts.evaluate('YHOO,AMZN')
	
In this case ``YAHOO`` and ``AMZN`` are two symbols which the data loader
must be able to handle, otherwise an error will occur.

The default data loader is :class:`dynts.TimeSerieLoader`.
To select a different one, simply pass it to the :func:`dynts.evaluate`
functions::

	>>> import dynts
	>>> import mydata.loader import customdataloader
	>>> ts = dynts.evaluate('YHOO,AMZN', loader = customdataloader)


The data loader Interface
==================================

.. autoclass:: dynts.TimeSerieLoader
   :members:
   :member-order: bysource