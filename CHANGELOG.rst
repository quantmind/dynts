
Version 0.3.4 - Development
================================
* Added sphinx_ extension in mod:`dynts.web.dyntsx` for displaying the list of timeseries functions available.
* Created the ``lib`` module where cython_ extensions will be placed. Cython extensions will be compiled only
  if cython is available, otherwise a fall-back pure python library will be used.
* Redesign of test suite. You can now run tests for given tags::

	python runtests dsl interface ...
	
  Each tag is defined by a directory in the :mod:`dynts.tests.regression` module.
* Added simple statistics pivot table.
* Bug fixes.
* **76 Tests**, **73% test coverage**

Version 0.3.3 - 2010 November 16
===================================
* Bug fix in :func:`dynts.TimeSeries.series` generator.
* **73 Tests**

Version 0.3.2 - 2010 October 20
======================================
* Development status set to ``Beta``.
* Added ``test`` module which implements shortcut functions for testing.
* Support for binary operations ``+-*\`` in place.
* Added ``series_info`` parameter to :ref:`flot formatter <formatters-flot>`.
* :ref:`Ecoplot plugin <ecoplot-web>` handles series options from server.
* More documentation.
* **10** ``dsl`` functions.
* **72 tests**. 

Version 0.3.1 - 2010 October 10
=================================
* Removed all dependencies from ``setup`` module.
* Added new :mod:`dynts.maths` module for mathematics and statistics.
* Passing ``request`` to :func:`dynts.web.views.TimeSeriesView.getdata`.
* Bug fix in :mod:`dynts.dsl` which was crashing the parser when using symbol names starting with a numeric value.
* **5** ``dsl`` functions.
* **61 tests**. 

Version 0.3.0 - 2010 October 06
==================================
* Added initial support for XY series in :class:`dynts.xydata`.
* :class:`dynts.TimeSeries` derived from :class:`dynts.DynData`.
* Added the :attr:`dynts.DynData.info` attribute for storing additional information about data. 
* Added a simple ``scatter`` function for performing scatter plots.
* Added logging parameter in :func:`dynts.evaluate`.
* Formatters are instances rather than functions.
* Can specify backend in :func:`dynts.evaluate`.
* Introduced :func:`dynts.tsname` for creating names for a mutivariate timeseries.
* Introduced :func:`dynts.merge` for merging two or more :class:`dynts.TimeSeries`.
* Refactored jQuery plugin ``ecoplot.js``.
* **5** ``dsl`` functions.
* **60 tests**. 

Version 0.2.0 - 2010 September 24
====================================
* Development moved to github http://github.com/quantmind/dynts
* Added skiplist python implementation.
* Added ccy_ to dependencies.
* **4** ``dsl`` functions.
* **53 tests**.

Version 0.1.0  - 2010 September 12
====================================
* First release to PyPi in pre-alpha.
 

.. _cython: http://www.cython.org/
.. _ccy: http://code.google.com/p/ccy/
.. _sphinx: http://sphinx.pocoo.org/