
===========================
Zoo
===========================


Timeserie backend based on the R package zoo_. The package provides infrastructure
for regularly and irregularly spaced time series using arbitrary
classes for the time stamps.

.. _zoo: http://cran.r-project.org/web/packages/zoo/index.html

To install zoo, launch R (R http_proxy=http://your.proxy.com if behind a proxy server)
and type::
	
	install.packages("zoo")
	
To create a ``zoo``-timeseries::

	import dynts
	ts = dynts.timeseries(