.. _index-dsl:

===========================
Domain Specific Language
===========================

.. _dsl-script:

Timeseries Expressions
============================

A light-weight domain specific language used to analyse  and modify
:class:`dynts.TimeSeries`.
Here few script examples:

* ``GOOG`` a :class:`dynts.dsl.Symbol` which creates one timeseries
* ``GOOG,YHOO`` two timeseries.
* ``2*GOOG`` a multiplication
* ``GOOG-AMZN`` a subtraction between two symbols.


.. _dsl-parse:

Parsing timeserie scripts
==============================
Parsing timeserie expression is accomplished using the :func:`dynts.parse` function:


.. autofunction:: dynts.parse


For example::

	>>> import dynts
	>>> r = dynts.parse('GOOG/2,YHOO')
	>>> r.type
	'concatenationop'
	>>> len(r)
	2

Now lets load some data using the built-in dataproviders::

	>>> result = dynts.evaluate(r)
	>>> result.expression
	goog / 2.0 , yhoo
	>>> ts = result.unwind()
	>>> len(ts)
	2
	

Abstract Syntax Nodes
================================

Expr
~~~~~~~~~~~~~~~

.. autoclass:: dynts.dsl.Expr
   :members:


Symbol
~~~~~~~~~~~~~~~~~~~

.. autoclass:: dynts.dsl.Symbol
   :members:
   
A symbol is any string expression which is not a function. For example::

	>>> e = dynts.parse('0.5*GOOG')
	>>> e[1].type
	'symbol'
	>>> e.symbols()
	[GOOG]
	
Symbols are special types of the abstract syntax tree which defines the timeserie DSL.
values of symbol are given by external data providers such as blooberg, yahoo finance, google finance
and so forth.
	
