.. _ecoplot-web:

=========================
Ecoplot JQuery Plugin
=========================

Dynts comes with a fully fledged jQuery_ plugin for manipulating
timeseries and scatter plots directly on the browser.
The plugin is located on the ``media`` directory.

Dependencies
==========================
There are two dependencies:

* jQuery_ javascript library.
* Flot_ javascript plotting library. For convenience, this library is shipped within the ``media`` directory.

The scripts to include are the followings::

	<script type="text/javascript" src=".../dynts/flot/excanvas.min.js"></script>
	<script type="text/javascript" src=".../dynts/flot/jquery.flot.js"></script>
	<script type="text/javascript" src=".../dynts/ecoplot/ecoplot.js"></script>
	
	
Getting Started
==========================
Lets say we have a tag in the HTML we want the plugin to be renered.
It is as easy as this::

	<div id="plot"></div>

	var eco = $('#plot').ecoplot();
	


Toolbar
=================

The toolbar is an array of toolbar items::
	
	var toolbar = [item1,...,itemN];
	

where a toolbar items is an object, for example::

	item = {
	    classname: 'zoomout',
	    title: "Zoom Out",
	    icon: "ui-icon-zoomout",
	    decorate: function(b,el) {...}
    }
	

.. _jQuery: http://jquery.com/
.. _flot: http://code.google.com/p/flot/



