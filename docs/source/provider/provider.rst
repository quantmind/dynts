.. _data-providers:

===========================
Data Providers
===========================

This section deals with loading data from `data providers`.
Data providers populate :class:`dynts.dsl.Symbol` instances with actual data.
For example::

	>>> import dynts
	>>> ts = dynts.evaluate('YHOO,AMZN')
	
In this case ``YAHOO`` and ``AMZN`` are two symbols which a least one of the
registered data provider will be able to handle, otherwise an error will occur.


Data provider interface
==================================

A data provider is a class which derives from :class:`dynts.data.DataProvider`
and is responsable for loading actual data into :class:`dynts.dsl.Symbol`.
A data provider can be a simple web service, your own data source or a professional
streaming source.

.. autoclass:: dynts.data.DataProvider
   :members:
   :member-order: bysource


Available Providers
==============================

Dynts is currently shipped with two providers:

* ``google`` finance
* ``yahoo`` finance

To check for registered providers::

	>>> from dynts.data import providers
	>>> providers.keys()
	['GOOGLE', 'YAHOO']
	

Registering
=================
Let's say we create a new provider along these lines::

	from dynts.data import DataProvider
	
	class MyCustomProvider(DataProvider):
	
	    def load(ticker, startdate, enddate, fields, logger):
	    	...
	
Registration is obtained simply::

	>>> from dynts.data import register
	>>> register(MyCustomProvider)
	>>> providers.keys()
	['MYCUSTOMPROVIDER', 'GOOGLE', 'YAHOO']

	 
	 