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
	
How do we deal with mismatching dates?