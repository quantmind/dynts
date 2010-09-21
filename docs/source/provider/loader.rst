.. _data-loader:

===========================
Data Loader
===========================

The default data loader is :class:`dynts.TimeSerieLoader`.
To select a different one, simply pass it to the :func:`dynts.evaluate`
functions::

	>>> import dynts
	>>> import mydata.loader import customdataloader
	>>> ts = dynts.evaluate('YHOO,AMZN', loader = customdataloader)


The data loader class
==================================

.. autoclass:: dynts.TimeSerieLoader
   :members:
   :member-order: bysource