.. _settings:

=====================
Settings
=====================

There is a ``setting`` object which can be modified at runtime to customize the dynts environment.
To access the object type::

	from dynts.conf settings
	
This is the list of attributes:

* ``backend`` the default timeserie backend to use. Default: ``zoo``.
* ``months_history`` the default number of months of history. Default: ``12``.
* ``proxies`` proxy dictionary. Default: ``{}``. If you need to use a proxy server to access the web::
	
	settings.proxies['http'] = 'http://yourproxy.com:80'