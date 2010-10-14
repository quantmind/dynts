Development
==================
* Added ``series_info`` parameter to :ref:`flot formatter <formatters-flot>`.
* :ref:`Ecoplot plugin <ecoplot-web>` handles series options from server.
* More documentation.
* **7** ``dsl`` functions.
* **61 tests**. 


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
 

.. _ccy: http://code.google.com/p/ccy/