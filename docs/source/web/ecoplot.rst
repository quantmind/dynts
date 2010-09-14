.. _ecoplot-web:

=========================
Ecoplot JQuery Plugin
=========================

Dynts comes with a fully fledged JQuery plugin for manipulating timeseries and scatter plots
directly on the browser. The plugin is located on the ``media`` directory.

Dependencies
==========================
There are two dependencies:

* jQuery__ javascript library.
* Flot__ javascript plotting library. For convenience, this library is shipped with dynts.

__ http://jquery.com/
__ http://code.google.com/p/flot/

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
	






