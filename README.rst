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
At the core of the library there is a Domain-Specific-Language (DSL_) dedicated
to timeserie analysis and manipulation. DynTS makes timeserie manipulation easy and fun.
This is a simple multiplication::
	
	>>> import dynts
	>>> e = dynts.parse('2*GOOG')
	>>> e
	2.0 * goog
	>>> len(e)
	2
	>>> list(e)
	[2.0, goog]
	>>> ts = dynts.evaluate(e).unwind()
	>>> ts
	timeserie:zoo:2.0 * goog
	>>> len(ts)
	251


Requirements
=====================
There are several requirements that must be met:

* numpy_ arrays and matrices.
* ply_ the building block of the DSL_.
* rpy2_ if an R_ timeserie back-end is used (default).
* ccy_ for date and currency manipulation.

Depending on the back-end used, additional dependencies need to be met.
For example, there are back-ends depending on the following R packages:

* zoo_ and PerformanceAnlytics_ for the ``zoo`` back-end (currently the default one)
* timeSeries_ for the ``rmetrics`` back-end 

Installing rpy2_ on Linux is straightforward, on windows it requires the
`python for windows`__ extension library.

Running Tests
=================
Form the package directory::
	
	python runtests.py
	
or, once installed::

	from dynts import runtests
	runtests()
	
.. _numpy: http://numpy.scipy.org/
.. _ply: http://www.dabeaz.com/ply/
.. _rpy2: http://rpy.sourceforge.net/rpy2.html
.. _DSL: http://en.wikipedia.org/wiki/Domain-specific_language
.. _R: http://www.r-project.org/
.. _ccy: http://code.google.com/p/ccy/
.. _zoo: http://cran.r-project.org/web/packages/zoo/index.html
.. _PerformanceAnlytics: http://cran.r-project.org/web/packages/PerformanceAnalytics/index.html
.. _timeSeries: http://cran.r-project.org/web/packages/timeSeries/index.html
__ http://sourceforge.net/projects/pywin32/files/
