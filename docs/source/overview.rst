.. _intro-overview:

=====================
Overview
=====================

.. rubric:: Timeserie analysis and a timeserie domain specific language written in Python.

**This package is under development, not a finish thing. You have been warned.**

Timeserie Object
========================

To create a timeserie object directly::

	>>> from dynts import timeserie
	>>> ts = timeserie('test')
	>>> ts.type
	'zoo'
	>>> ts.name
	'test'
	>>> ts
	timeserie:zoo:test
	>>> str(ts)
	'test'

DSL
=======

DynTS makes timeserie manipulation easy and fun. This is a simple multiplication::
	
	>>> import dynts
	>>> e = dynts.parse('2*GOOG')
	>>> e
	2.0 * GOOG
	>>> len(e)
	2
	>>> list(e)
	[2.0, GOOG]
	
	
Requirements
================

The library is dependent on three Python packages
 * numpy__
 * rpy2__
 * python-dateutil__
 
and it is also dependent on several R packages, depending on the back-end used.
These two are always needed:
 * zoo__
 * PerformanceAnlytics__

__ http://www.numpy.org/
__ http://rpy.sourceforge.net/rpy2.html
__ http://labix.org/python-dateutil
__ http://cran.r-project.org/web/packages/zoo/index.html
__ http://cran.r-project.org/web/packages/PerformanceAnalytics/index.html
