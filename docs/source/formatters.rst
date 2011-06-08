.. _formatters:

.. module:: dynts.formatters

=================================
Formatters
=================================

Dump a :class:`dynts.TimeSeries` instance into different formats.
Let's say we have a time series object ``ts``::

	s = ts.dump('flot', **kwargs)
	
will create a :class:`dynts.web.flot.MultiPlot` instance
for producing nice looking javascript graphs with flot_.
 
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

.. _formatters-flot:

Flot
~~~~~~~~~~
The flot format is used by the ``ecoplot`` jQuery plugin in ``dynts.web`` module.
The ``dump`` function accepts the following key-value parameters:

* ``desc`` if ``True`` the order of dates will be descending. Default ``False``.
* ``series_info`` dictionary with additional series parameters for flot.


VBA
~~~~~~~~~~~
The flot format is used to send JSON to VBA for displaying in an excel Worksheet.


CSV
~~~~~~~~~~~~~

Dump data into a ``csv`` stream::

    >>> f = open('test.csv','w')
    >>> f.write(ts.dump('csv'))
    >>> f.close()


XLS
~~~~~~~~~~~~~~~~

Dump timeseries into spreadsheet files that are are compatible with Excel,
OpenOffice.org Calc, and Gnumeric.
It requires the xlwt_ python package.

.. _xlwt: http://pypi.python.org/pypi/xlwt
.. _flot: http://code.google.com/p/flot/


Matplotlib
~~~~~~~~~~~~~~~~

A python formatter for plotting data on a matplotlib_ pyplot::

    >>> plt = ts.dump('plot')
    >>> plt.show()


.. _xlwt: http://pypi.python.org/pypi/xlwt
.. _flot: http://code.google.com/p/flot/
.. _matplotlib: http://matplotlib.sourceforge.net/
