.. _ecoplot-web:

=========================
Ecoplot JQuery Plugin
=========================

Dynts comes with a fully fledged jQuery_ plugin for manipulating
timeseries and scatter plots directly on the browser.
The plugin is located on the ``media/dynts/ecoplot`` directory.


.. _ecoplot-web-dep:

Dependencies
==========================
There are two dependencies:

* jQuery_ javascript library.
* Flot_ javascript plotting library. For convenience, this library is shipped within the ``media/dynts/flot`` directory.

The scripts to include are the followings::

	<script type="text/javascript" src=".../dynts/flot/excanvas.min.js"></script>
	<script type="text/javascript" src=".../dynts/flot/jquery.flot.min.js"></script>
	<script type="text/javascript" src=".../dynts/flot/jquery.flot.selection.min.js"></script>
	<script type="text/javascript" src=".../dynts/ecoplot/ecoplot.js"></script>
	

.. _ecoplot-web-intro:

Getting Started
==========================
Lets say we have a tag in the HTML we want the plugin to be rendered.
It is as easy as this::

	<div id="plot"></div>

	var eco = $('#plot').ecoplot(options);
	
where options is an objects containing parameters for the plugin.

Input Options
~~~~~~~~~~~~~~~~~~~~
.. js:attribute:: options.autoload

	If ``True`` (default) data is loaded when the plugin is created. 

.. js:attribute:: options.requestMethod

	Type of AJAX request to send to server for obtaining data. Default ``get``.
	
.. js:attribute:: options.responsetype

	Type of response from server. Currently only ``json`` is supported.
	

Output Options
~~~~~~~~~~~~~~~~~~~~~
The ``options`` object is updated with information useful for data manipulation.

.. js:attribute:: options.canvases

	Object containing information regarding canvases and data::
	
		canvases = {
			all: array of canvas,
			current: index of currenct canvas
			height: height of canvas in pixels
		}

.. _ecoplot-web-api:

API
=================

Attributes
~~~~~~~~~~~~~~~~~

.. js:attribute:: $.ecoplot.plugin_class
	
	Default: ``"econometric-plot"``
	
	Css class name to add to plugins ``div`` elements.
	
.. js:attribute:: $.ecoplot.version

	Version string.

addEvent
~~~~~~~~~~~~~

Add a custom event to the plugin. Check the :ref:`events <ecoplot-web-events>` documentation
for further information.

.. js:function:: $.ecoplot.addEvent({id:idname,register:reg_handler})

	:param string idname: A unique string to use as key for the event.
	:param reg_handler: A function called when registering the event with the plugin.
	

addMenu
~~~~~~~~~~~

Add custom action to the :ref:`menu bar <ecoplot-web-menubar>`.


paginate
~~~~~~~~~~~~~
Render the plugin.

removeEvent
~~~~~~~~~~~~~~~

Opposite to :js:func:`$.ecoplot.addEvent`, it removes an event from the registry.

.. js:function:: $.ecoplot.removeEvent(id)

	:param string idname: id of event to remove
	
.. _ecoplot-web-toolbar:

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
	
.. _ecoplot-web-events:

Events
====================

Registering events with the plugin is also fully supported::

	$.ecoplot.addEvent(event_handler);
	
where ``event_handler`` is an object with the following properties::

	event_handler = {
	    id: "unique_string_id",
	    register: function(el) {
	    ...
	    }
	}

where ``el`` is the ``jQuery`` element holding the plugin.
The ``register`` function implements the event handling
on the ``el`` element.
By default there are four registered events:

* ``load`` for loading data.
* ``zoom`` for zooming functionalities.
* ``datepicker`` for decorating date inputs with jQuery datepicker_ plugin.
* ``tooltip`` for showing tooltip in the canvas.


.. _ecoplot-web-menubar:

Menu Bar
====================

The menu is where we can add more interactive features with your data. To add menu
items you need to use the ``addMenu`` function::

	$.ecoplot.addMenu(menu_handler);
	
where ``menu_handler`` is an object with the following properties::

	menu_handler = {
	    name: 'unique_string_name',
	    classname: 'a css class name',
	    create: function(elem) {
	    ...
	    }
	};


.. _jQuery: http://jquery.com/
.. _flot: http://code.google.com/p/flot/
.. _datepicker: http://jqueryui.com/demos/datepicker/


.. _ecoplot-web-internals:

Internals
====================

Here we describe the internal functions which are not exposed via the API.

.. js:function:: _registerEvents

	called during initalization, it binds all events registered
	with :ref:`addEvent <ecoplot-web-events>` API function with the
	ecoplot element.

.. js:function:: _set_new_canavases($this,data)

	Called after new data arrives, it updates the current canvases or create new ones.
	:param object $this: jQuery object holding the plugin
	:param object $this: list of flot-type objects containg data and plotting options.
	
.. js:function:: _add(options, el_, data_, oldcanvas)

	Create a flot canvas for a plugin.
	
	
.. js:function:: _editpannel

	for creating editing panels 