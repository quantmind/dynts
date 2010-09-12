
===========================
R-Metrics
===========================


Timeserie backend based on the R-metrics__ package timeSeries__. The timeSeries
package provides a S4 class definition for univariate and multivarate analysis.

To install timeSeries, launch R (R http_proxy=http://your.proxy.com if behind a proxy server)
and type::
	
	install.packages("timeSeries")
	

From an implementation perspective, the rmetrics timeserie backend is different from the zoo
implementation because of RS4 objects  are a little more formal regarding their class definition,
and all instances belong to the low-level R type SEXPS4.



__ https://www.rmetrics.org/
__ http://cran.r-project.org/web/packages/timeSeries/index.html