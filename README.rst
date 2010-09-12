:Documentation: http://packages.python.org/dynts/
:Dowloads: http://pypi.python.org/pypi/dynts/
:Source: http://github.com/quantmind/dynts
:Keywords: timeserie, quantitative, finance, statistics

--

Timeserie analysis and a timeserie domain specific language written in Python.


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
=====================

* numpy__
* ply__
* rpy2__
* ccy__
 
and it is also dependent on several R packages, depending on the back-end used.
These two are always needed:

* zoo__
* PerformanceAnlytics__


Running Tests
=================
Form the package directory::
	
	python runtests.py
	
or, once installed::

	from dynts import runtests
	runtests()
	
	
__ http://numpy.scipy.org/
__ http://www.dabeaz.com/ply/
__ http://rpy.sourceforge.net/rpy2.html
__ http://code.google.com/p/ccy/
__ http://cran.r-project.org/web/packages/zoo/index.html
__ http://cran.r-project.org/web/packages/PerformanceAnalytics/index.html
	
