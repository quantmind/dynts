.. _index-dsl:

===========================
Domain Specific Language
===========================

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
	

.. _dsl-expr:

Expr
===========

.. autoclass:: dynts.Expr
   :members:


.. _dsl-symbol:

Symbol
===============
A symbol is any string expression which is not a function. For example::

	>>> e = dynts.parse('0.5*GOOG')
	>>> e[1].type
	'symbol'
	>>> e.symbols()
	[GOOG]
	
Symbols are special types of the abstract syntax tree which defines the timeserie DSL.
values of symbol are given by external data providers such as blooberg, yahoo finance, google finance
and so forth.
	
