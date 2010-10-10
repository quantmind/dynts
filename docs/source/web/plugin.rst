.. _djpcms-web:

===============================
Using with Django and Djpcms
===============================

This section explains how to use the :ref:`ecoplot <ecoplot-web>` jQuery plugin
on a django_ powered site which uses djpcms_ as content
management system.

First you need to install djpcms_ and add it to the installed applications of
your django project. Second, add the ``dynts.web.plugins`` to the ``DJPCMS_PLUGINS``.
The settings file should contains::

	INSTALLED_APPLICATIONS += ('djpcms','dynts',)
	DJPCMS_PLUGINS.append('dynts.web.plugins')


TimeSeries View
=======================

.. autoclass:: dynts.web.views.TimeSeriesView
   :members:
   :member-order: bysource
   

.. _jQuery: http://jquery.com/
.. _django: http://www.djangoproject.com/
.. _djpcms: http://github.com/lsbardel/djpcms
.. _AJAX: http://en.wikipedia.org/wiki/Ajax_(programming)