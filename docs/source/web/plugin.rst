
=========================
Using with Djpcms
=========================

First you need to install djpcms__ and add it to the installed applications of
your django project. Second, add the ``dynts.web.plugins`` to the ``DJPCMS_PLUGINS``.
The settings file should contains::

	INSTALLED_APPLICATIONS += ('djpcms','dynts',)
	DJPCMS_PLUGINS.append('dynts.web.plugins')


__ http://github.com/lsbardel/djpcms