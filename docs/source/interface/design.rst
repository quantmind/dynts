.. _design-choices:


========================
Design Choices
========================

Here are outlined the design choices which have been taken during
the development of the library.


TimeSeries Operations
===========================
Let's say we have two timeseries objects ``ts1`` and ``ts2`` and need to obtain
a new timeseries which contains as values the sum of the two::

	ts = ts1+ts2
	
Mismatching dates
-------------------

In situations where an operation is performed on two timeseries it can not assumed that the same dates are present in both series.

To allow for this there need to be suitable timeseries operators, which allow the user to specify the necessary settings. Where standard mathematical binary operators are used such as ( + - / *), suitable defaults will be assumed.

An example of a timeseries operators include::
    
    >>>import operators
    >>>ts = operators.add(ts1, ts2, all = True, fill = None) 
    >>>#all indicates all dates are included
    ...#fill indicates the value to use for missing value. It can be a primitive or a class
    >>>


