.. _index-dsl:

===========================
Domain Specific Language
===========================

.. _dsl-parse:

parse
===========

.. autofunction:: dynts.dsl.parse


.. _dsl-expr:

Expr
===========

.. autoclass:: dynts.dsl.Expr
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
	
