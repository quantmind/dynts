.. _backends:

===========================
Timeserie Backends
===========================


Numpy
===============

This is the default backend.


R Zoo
===========================

Timeserie backend based on the R package zoo_. The package provides infrastructure
for regularly and irregularly spaced time series using arbitrary
classes for the time stamps.

To use the zoo_ backend you need to install rpy2_, a package for embedding
R into python::

    pip install rpy2

To install zoo, launch R (R http_proxy=http://your.proxy.com if behind a proxy server)
and type::
    
    install.packages("zoo")
    
To create a ``zoo``-timeseries::

    >>> import dynts
    >>> ts = dynts.timeseries(backend = 'zoo')
    >>> ts.type
    'zoo'
    

R-Metrics
===========================

Timeserie backend based on the R-metrics_ package timeSeries_. The timeSeries
package provides a S4 class definition for univariate and multivarate analysis.

To install timeSeries, launch R (R http_proxy=http://your.proxy.com if behind a proxy server)
and type::
    
    install.packages("timeSeries")
    

From an implementation perspective, the rmetrics timeserie backend is different from the zoo
implementation because of RS4 objects  are a little more formal regarding their class definition,
and all instances belong to the low-level R type SEXPS4.


.. _numpy: http://numpy.scipy.org/
.. _rpy2: http://rpy.sourceforge.net/rpy2.html
.. _zoo: http://r-forge.r-project.org/projects/zoo/
.. _R-metrics: https://www.rmetrics.org/
.. _timeSeries: http://cran.r-project.org/web/packages/timeSeries/index.html
