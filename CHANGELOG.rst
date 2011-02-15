Ver. 0.4.0 - 2011 Feb 15
================================
* Dropped python 2.5 compatibility and moved towards python 3 support. The idea is to
  have the library working on python 2.6, 2.7 and the 3 series by the next version.
* Regular expression for ``DSL`` IDs changed to::

    r'`[^`]*`|[a-zA-Z_][a-zA-Z_0-9:@]*'
     
* Moved ``tests`` module outside ``dynts`` package. It now contains three types of tests:
  
  * ``regression`` for unit and regression tests.
  * ``profile`` for analysing performance of different backends and impact of cython_.
  * ``bench`` same as ``profile`` but geared towards speed rather than profiling.
  Check :ref:`Running tests <running-tests>` for more information.  	
* Added fallback tests and split ``zoo`` and ``numpy`` timeseries backend tests.
* Added sphinx_ extension in :mod:`dynts.web.dyntsx` for displaying the list of timeseries functions available.
* Created the ``lib`` module where cython_ extensions will be placed. Cython extensions will be compiled only
  if cython is available, otherwise a fall-back pure python library will be used.
* Added simple statistics pivot table.
* Bug fixes.
* **118 Tests**, **70% test coverage**

Ver. 0.3.3 - 2010 Nov 16
===================================
* Bug fix in :func:`dynts.TimeSeries.series` generator.
* **73 Tests**

Ver. 0.3.2 - 2010 Oct 20
======================================
* Development status set to ``Beta``.
* Added ``test`` module which implements shortcut functions for testing.
* Support for binary operations ``+-*\`` in place.
* Added ``series_info`` parameter to :ref:`flot formatter <formatters-flot>`.
* :ref:`Ecoplot plugin <ecoplot-web>` handles series options from server.
* More documentation.
* **10** ``dsl`` functions.
* **72 tests**. 

Ver. 0.3.1 - 2010 Oct 10
=================================
* Removed all dependencies from ``setup`` module.
* Added new :mod:`dynts.maths` module for mathematics and statistics.
* Passing ``request`` to :func:`dynts.web.views.TimeSeriesView.getdata`.
* Bug fix in :mod:`dynts.dsl` which was crashing the parser when using symbol names starting with a numeric value.
* **5** ``dsl`` functions.
* **61 tests**. 

Ver. 0.3.0 - 2010 Oct 06
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

Ver. 0.2.0 - 2010 Sep 24
====================================
* Development moved to github http://github.com/quantmind/dynts
* Added skiplist python implementation.
* Added ccy_ to dependencies.
* **4** ``dsl`` functions.
* **53 tests**.

Ver. 0.1.0  - 2010 Sep 12
====================================
* First release to PyPi in pre-alpha.
 

.. _cython: http://www.cython.org/
.. _ccy: http://code.google.com/p/ccy/
.. _sphinx: http://sphinx.pocoo.org/
