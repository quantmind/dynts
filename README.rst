
.. rubric:: A statistic package for python with enphasis on timeseries analysis.
            Built around numpy_, it provides several back-end timeseries classes
            including R-based objects via rpy2_.
            It is shipped with a domain specific language for timeseries analysis
            and manipulation.

--

:Documentation: http://packages.python.org/dynts/
:Dowloads: http://pypi.python.org/pypi/dynts/
:Source: http://github.com/quantmind/dynts
:Keywords: timeseries, quantitative, finance, statistics, numpy, R, web

--


.. contents::
    :local:


Timeserie Object
========================

To create a timeseries object directly::

	>>> from dynts import timeseries
	>>> ts = timeseries('test')
	>>> ts.type
	'zoo'
	>>> ts.name
	'test'
	>>> ts
	TimeSeries:zoo:test
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
	TimeSeries:zoo:2.0 * goog
	>>> len(ts)
	251


Requirements
=====================
There are several requirements that must be met:

* python_ 2.6 or later. Support for Python 3 series is under development and should be completed soon.
* numpy_ version 1.5.1 or higher for arrays and matrices.
* ply_ version 3.3 or higher, the building block of the DSL_.
* rpy2_ if an R_ TimeSeries back-end is used (default).
* ccy_ for date and currency manipulation.

Depending on the back-end used, additional dependencies need to be met.
For example, there are back-ends depending on the following R packages:

* zoo_ and PerformanceAnlytics_ for the ``zoo`` back-end (currently the default one)
* timeSeries_ for the ``rmetrics`` back-end 

Installing rpy2_ on Linux is straightforward, on windows it requires the
`python for windows`__ extension library.

Optional Requirements
===============================

* cython_ for performance. The library is not strictly dependent on cython, however its usage
  is highly recommended. If available several python modules will be replaced by more efficient compiled C code.
* xlwt_ to create spreadsheet from timeseries.
* matplotlib_ for plotting.
* djpcms_ for the ``web.views`` module.

__ http://sourceforge.net/projects/pywin32/files/


.. _running-tests:

Running Tests
=================
There are three types of tests available:

* ``regression`` for unit and regression tests.
* ``profile`` for analysing performance of different backends and impact of cython_.
* ``bench`` same as ``profile`` but geared towards speed rather than profiling.
  
From the distribution directory type::
	
	python runtests.py
	
This will run by default the regression tests. To run a profile test
type::

	python runtests.py -t profile <test-name>
	
where ``<test-name>`` is the name of a profile test.
To obtain a list of available tests for each test type, run::

	python runtests.py --list

for regression, or:: 

	python runtests.py -t profile --list
	
for profile, or::

	python runtests.py -t bench --list
	
from benchmarks.
	
If you access the internet behind a proxy server, pass the ``-p`` option, for example::

	python runtests.py -p http://myproxy.com:80

It is needed since during tests some data is fetched from google finance.

To access coverage of tests you need to install the coverage_ package and run the tests using::

	coverage run runtests.py
	
and to check out the coverage report::

	coverage report -m
	

Kudos
===========
* numpy_ developers.


Community
=================
Trying to use an IRC channel **#dynts** on ``irc.freenode.net``
(you can use the webchat at http://webchat.freenode.net/).

If you find a bug or would like to request a feature, please `submit an issue`__.

__ http://github.com/quantmind/dynts/issues
    
.. _numpy: http://numpy.scipy.org/
.. _ply: http://www.dabeaz.com/ply/
.. _rpy2: http://rpy.sourceforge.net/rpy2.html
.. _DSL: http://en.wikipedia.org/wiki/Domain-specific_language
.. _R: http://www.r-project.org/
.. _ccy: http://code.google.com/p/ccy/
.. _zoo: http://cran.r-project.org/web/packages/zoo/index.html
.. _PerformanceAnlytics: http://cran.r-project.org/web/packages/PerformanceAnalytics/index.html
.. _timeSeries: http://cran.r-project.org/web/packages/timeSeries/index.html
.. _Python: http://www.python.org/
.. _xlwt: http://pypi.python.org/pypi/xlwt
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _djpcms: http://djpcms.com
.. _coverage: http://nedbatchelder.com/code/coverage/
.. _cython: http://www.cython.org/
