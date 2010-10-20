.. _data-loader:

===========================
Data Loader
===========================
A data loader object coordinates which data provider to use and provides hooks
for pre-processing, post-processing and storing data on your database if required.
 
The default data loader is :class:`dynts.data.TimeSerieLoader`.
To select a different one, simply pass it to the :func:`dynts.evaluate`
functions::

	>>> import dynts
	>>> import mydata.loader import customdataloader
	>>> ts = dynts.evaluate('YHOO,AMZN', loader = customdataloader)

Alternatively, one can specify a new loader in the :ref:`settings <settings>`::

	>>> from dynts.conf import settings
	>>> settings.default_loader = customdataloader

The data loader class
==================================

.. autoclass:: dynts.data.TimeSerieLoader
   :members:
   :member-order: bysource