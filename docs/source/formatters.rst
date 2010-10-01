.. _formatters:

=================================
Formatters
=================================

Dump a :class:`dynts.TimeSeries` instance into different format.
Let's say we have a time series object ``ts``::

	s = ts.dump('flot')
	
check :class:`dynts.DynData.dump`.


Registering Formatters
=============================

To register new way of formatting timeseries::

	from dynts import Formatters
	
	Formatters['newformat'] = your_formatting_function
	
where ``your_formatting_function`` takes the ``ts`` as positional input and
any other ``key-value`` parameters.

You can use the new function::

	ts.dump('newformat')


Available Formatters
===========================

There are two JSON formatters: ``flot`` and ``vba``. They both return JSON strings
but in different formats.

Flot
~~~~~~~~~~
The flot format is used by the ``ecoplot`` jQuery plugin in ``dynts.web`` module.


VBA
~~~~~~~~~~~
The flot format is used to send JSON to VBA for displaying in an excel Worksheet.


CSV
~~~~~~~~~~~~~



XLS
~~~~~~~~~~~~~~~~

Dump timeseries into spreadsheet files that are are compatible with Excel,
OpenOffice.org Calc, and Gnumeric.
It requires the xlwt_ python package.

.. _xlwt: http://pypi.python.org/pypi/xlwt

