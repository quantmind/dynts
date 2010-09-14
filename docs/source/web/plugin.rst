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

.. class:: dynts.web.views.TimeSeriesView

	Derived from :class:`djpcms.views.appview.AppView`.
	The only response method available is an AJAX_ Get.
	
	.. function:: get_response(djp)
	
		Returns an HttpResponse object of *mimetype* ``application/javascript``.
		
	.. function:: getdata(code, start, end, **kwargs)
	
		Pure virtual function which needs to be implemented by implementations.
		It retrieve the actual timeseries data.
		
		* *code* a :ref:`timeseries expressions <dsl-script>` to be evaluated.
		* *start* start date
		* *end* end date
		
	.. function:: get_object(code)
	
		Check if the code is an instance of the view underlying model.
		If that is the case it returns the object, otherwise it returns ``None``.


.. _jQuery: http://jquery.com/
.. _django: http://www.djangoproject.com/
.. _djpcms: http://github.com/lsbardel/djpcms
.. _AJAX: http://en.wikipedia.org/wiki/Ajax_(programming)