.. functions:

==========================
Functions
==========================

This section lists all the functions available within the
:ref:`domain specific language <index-dsl>`. Each function can
be called stand-alone or in combination with other others as long as
the grammar of the language is respected.


In the following list we assume the following shortcuts:

.. math::

	\Delta x_t &= \Delta_1 x_t = x_t - x_{t-1}\\
	\Delta^2 x_t &= \Delta_1^2 x_t = \Delta_1 x_t - \Delta_1 x_{t-1}


The function documentation is build from the source code, using the sphinx 
macro ``dyntslist`` defined in :mod:`dynts.web.dyntsx`.


.. dyntslist::
