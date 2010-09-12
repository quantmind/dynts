/* 
 * Econometric Plot Plugin
 * 
 * version: 0.1
 * 
 * @requires jQuery v1.2.2 or later
 * @requires flot
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * Revision: $Id$
 */
(function($) {

/*
    Usage Note:  
    -----------
      
*/

$.extend({
	ecoplot: new function() {
		var extraTools     = {};
		var events         = {};
		var debug		   = false;
		
		var default_command_line = {
		    css:		 null,
		    show:		 true,
		    symbol:	 	 null,
		    showperiod:	 false,
		    periodlabel: 'Period'
		};
		
		this.defaults = {
			show:			true,
			responcetype:   'json',
			requestMethod:  'get',
			elems:			{},
			commandline:	default_command_line,
			requestParams: 	{},
		    date_format: 	"d M yy",
		    autoload:		true,
		    load_url:		null,
		    loaderimage:	'ajax-loader.gif',
		    flot_options:	{
							xaxis: {}
							},
		    paginate:		null,
		    infoPanel:		'ecoplot-info',
		    defaultFade:	300,
		    actions:		 ['zoom', 'reload', 'datepicker'],
		    default_month_interval: 12,
		    classname:		 'ts-plot-module',
		    errorClass:		 'dataErrorMessage',
		    canvasClass:	 'ts-plot-module-canvas',
		    convasContClass: 'ts-plot-module-canvas-container',
		    inputDateClass:	 'ts-input-date',
		    startLoading:	function($this) {
		    	var co = this.elems;
		    	co.loader.css({'display':'block'});
				co.canvas_cont.css({'opacity':'0.4'});
		    },
			stopLoading: 	function($this) {
		    	var co = this.elems;
		    	co.loader.css({'display':'none'});
				co.canvas_cont.css({'opacity':'1'});
		    },
		    parse: null
		};
		
		/**
		 * Logger function during debug
		 */
		function log(s) {
			if(debug) {
				if (typeof console != "undefined" && typeof console.debug != "undefined") {
					console.log(s);
				} else {
					//alert(s);
				}
			}
		}
		
		function _addelement(el,holder) {
			 var id  = el.id.toLowerCase();
			 var p   = holder[id];
			 if(!p) {
				 el.id = id;
				 holder[id] = el;
			 }
		}
		
		function _parseOptions(options_, defaults) {
			var options = {
					load_url: null,
					elems: {}
					};
			$.extend(true, options, defaults);
			$.extend(true, options, options_);
			
	        var cl = options.commandline;
	        if(!cl) {
	        	cl = default_command_line;
	        	options.commandline = cl;
	        }
	        if(cl.symbol) {
	        	cl.show = false;
	        }
	        return options;
		}
		
		function _set_default_dates($this)  {
			var options = $this.options;
	    	var td = new Date();
	    	var v2 = $.datepicker.formatDate(options.date_format, td);
	    	td.setMonth(td.getMonth() - options.default_month_interval);
	    	var v1 = $.datepicker.formatDate(options.date_format, td);
	    	var elems = options.elems;
	    	if(elems) {
	    		elems.start.val(v1);
	    		elems.end.val(v2);
	    	}
	    }
		
		function _registerEvents($this) {
			var elems = $this.options.elems;
			
			$(window).resize(function() {
	        	if(elems.canvas && elems.canvas.render)  {
	        		elems.canvas.render();
	        	}
	        });
			
			var actions = $this.options.actions;
			$.each(actions, function(i,v) {
				var eve = events[v];
				if(eve) {
					log('Registering event '+v);
					eve.register($this);
				}
    		});
    	}
		
		function _get_data($this)  {
			var elems = $this.options.elems;
			var ticker = elems.commandline.val()
			if(!ticker) {return null;}
			return {
				start:elems.start.val(),
				end:elems.end.val(),
				period:'',
				command:ticker
			};
		}
		
		/**
		 * Internal function for setting up the plot.
		 * @param data, Array of plot objects
		 */
		function _set_new_canavases($this,data) {
			var options = $this.options;
			var elems   = options.elems;
			var outer     = $('<div></div>');
			var container = elems.canvas_cont;
			var c         = container.children();
			c.fadeOut(options.defaultFade).remove();
			//var wrap = $('<div></div>').css({'width':'100%','overflow':'hidden'}).appendTo(container);
			var outer = $('<div></div>').appendTo(container);
			var newcanvases = [];
			var datac,typ;
			
			var height = $this.height();
			$this.height(height);
			
			function _add(el_, data_) {
				el_.addClass(options.canvasClass);
				var typ = data_.type;
				log('Rendering '+ typ + ' data.');
				
				var renderflot = function(opts) {
					var zoptions;
					if(opts) {zoptions = $.extend(true, {}, this.options, opts);}
					else {zoptions = this.options;}
					this.elem.height(options.height);
					this.flot = $.plot(this.elem, this.series, zoptions);
					return this;
				}
				
				data_.elem = el_;
				data_.render = null;
				
				newcanvases.push(data_);
				
				if(typ == 'timeseries') {
					data_.options = $.extend(true, {}, options.flot_options);
					data_.options.xaxis.mode = 'time';
					data_.render = renderflot;
				}
			}
			
			if(data) {
				var width;
				if(data.length == 1) {
					width = outer.width();
					_add(outer,data[0]);
				}
				else {
					var cid, cv
					var ul = $('<ul></ul>').appendTo(outer);
					$.each(data, function(i,v) {
						cid = 'canvas' + i;
						ul.append($('<li><a href="#' + cid + '">' + v.label + '</a></li>'));
						cv  = $('<div></div>').attr('id',cid);
						outer.append(cv);
						_add(cv,v);
					});
					outer.tabs();
				}
				elems.canvas = newcanvases[0];
			}
			else {
				elems.canvas = null;
			}
			elems.canvases = newcanvases;
			$this.height('auto');
			
			if(elems.canvas) {
				elems.canvas.render();
			}
		}
		
		/**
		 * Render data.
		 * @param $this, the ecoplot element
		 * @param data, Array of plot canvases
		 * 
		 * }
		 */
		function _finaliseLoad($this,data) {
			var options = $this.options
			var elems = $this.options.elems;
			if(elems.info) {
				elems.info.html("");
			}
			_set_new_canavases($this, data);
			/*
			if(!data.success) {
				log('Server error. Data contains errors.');
				if(elems.info) {
					$.each(data.errors,function(i,v) {
						elems.info.append($('<p></p>').html(v).addClass(options.errorClass));
					});
				}
				_set_new_canavases($this);
			}
			else {
				_set_new_canavases($this,data.result);
			}
			*/
		}
		
		function _request($this)  {
	 		var options  = $this.options;
	 		if(!options.load_url)  {return;}
	 		var dataplot = _get_data($this);
	 		if(!dataplot) {return;}
	 		log("Preparing to send ajax request to " + options.load_url);
	 		var params   = {
	 			timestamp: +new Date()
	 		};
	 		$.each(options.requestParams, function(key, param) {
	 				params[key] = typeof param == "function" ? param() : param;
	 		});
	 		params = $.extend(true, params, dataplot);
	 		options.startLoading($this);
	 		$.ajax({url: options.load_url,
	 				type: options.requestMethod,
	 				data: $.param(params),
	 				dataType: options.responcetype,
	 				success: function(data) {
						log("Got the response from server");
						var ok = true;
						if(options.parse)  {
							try {
								data = options.parse(data,$this);
							}
							catch(e) {
								ok = false;
								log("Failed to parse data. " + e);
							}
						}
						options.stopLoading($this);
						if(ok)  {
							try {
								_finaliseLoad($this,data);
							}
							catch(e) {
								log("Failed to plot data. " + e);
							}
						}
					}
	 		});
	 	}
	        
		/**
		 * Constructor
		 */
		function _construct(options_) {
			var options = _parseOptions(options_, $.ecoplot.defaults);
			return this.each(function() {
				var $this = $(this);
				$this.options = options;
				$this.hide().html("");
				
				// Pagination
				if(options.paginate) {
					options.paginate($this);
				}
				else if($.ecoplot.paginate) {
					$.ecoplot.paginate($this);
				}
				
				_registerEvents($this);
				
				if(options.autoload) {
					$.ecoplot.loadData($this);
				}
				if(options.show) {
					$this.fadeIn(options.defaultFade);
				}
			});
		}
		
		
		/////////////////////////////////////////////////////////////////
		//		API FUNCTIONS
		/////////////////////////////////////////////////////////////////
		this.construct			= _construct;
		this.paginate  		   	= null;
		this.set_default_dates 	= _set_default_dates;
		this.loadData    		= _request;
		this.addEvent	    	= function(e){_addelement(e,events)};
		this.debug		   		= function(){return debug;};
		this.setdebug	   		= function(v){debug = v;};
		this.log			 	= log;
	}
});



$.fn.extend({
    ecoplot: $.ecoplot.construct
});



var ecop = $.ecoplot;


///////////////////////////////////////////////////
//	SOME ACTIONS
///////////////////////////////////////////////////
ecop.addEvent({
	id: 'zoom',
	className: 'zoom-out',
	register: function($this) {
		var comm;
		var options = $this.options;
		var menu    = options.elems.actionsmenu;
		if(menu) {
			
			var el = $(document.createElement("a"))
					.attr({'title':'Zoom out'})
					.addClass(this.className);
			menu.append($(document.createElement("li")).append(el));
			el.click(function(e) {
				var pl = options.elems.canvas;
				if(pl) {
					pl.render();
				}
			});
			
			$this.bind("plotselected", function (event, ranges) {
				var pl = options.elems.canvas;
				if(!pl) {
					return;
				}
	    		function checkax(ax)  {
	    			if(ax.to - ax.from < 0.00001)  {
	    				ax.to = ax.from + 0.00001;
	    			}
	    			return {min: ax.from, max: ax.to};
	    		}
	    		var ax = pl.flot.getAxes();
	    		var opts = {};
	    		if(ax.xaxis.used)  {
	    			opts.xaxis = checkax(ranges.xaxis);
	    		}
	    		if(ax.yaxis.used)  {
	    			opts.yaxis = checkax(ranges.yaxis);
	    		}
	    		if(ax.x2axis.used)  {
	    			opts.x2axis = checkax(ranges.x2axis);
	    		}
	    		if(ax.y2axis.used)  {
	    			opts.y2axis = checkax(ranges.y2axis);
	    		}
	            // do the zooming
	            pl.render(opts);
	            // don't fire event on the overview to prevent eternal loop
	            //overview.setSelection(ranges, true);
	    	});
		}
	}
});

ecop.addEvent({
	id: 'reload',
	className: 'reload',
	register: function($this) {
		var comm;
		var menu = $this.options.elems.actionsmenu;
		if(menu) {
			var el = $(document.createElement("a"))
					.attr({'title':'Reload data'})
					.addClass(this.className);
			menu.append($(document.createElement("li")).append(el));
			el.click(function(e) {
				$this.trigger('pre-reload',[this, $this]);
				$.ecoplot.loadData($this);
			});
		}
	}
});

ecop.addEvent({
	id: 'datepicker',
	register: function($this) {
	var options = $this.options;
		$('.'+options.inputDateClass,$this).datepicker({
			defaultDate: +0,
			showStatus: true,
			beforeShowDay: $.datepicker.noWeekends,
			dateFormat: options.date_format, 
		    firstDay: 1, 
		    changeFirstDay: false
		    //statusForDate: highlightToday, 
		    //showOn: "both", 
		    //buttonImage: prosp._classConfig.media_files_url + "img/icons/calendar_edit.png",
		    //buttonImageOnly: true
		});
	}
});



///////////////////////////////////////////////////
//		PAGINATION
///////////////////////////////////////////////////
ecop.paginate = function($this) {
	var options = $this.options;
	var elems   = options.elems;
	
	var _cl     = function(name) {
		return name;
		//return options.classname + '-' + name;
	};
	
	page = $(document.createElement("div")).addClass(_cl("main"));
	elems.canvas_cont  = $(document.createElement("div")).addClass(options.convasContClass);
	elems.page_options = $(document.createElement("div"))
							.addClass(_cl("options"))
							.css({'display':'none'});
	elems.loader	   = $(document.createElement("div")).css({'display':'none'}).append(
			$(document.createElement("a")).addClass('loader')
			.attr({'title':'Loading data'}));
	elems.html_options = $(document.createElement("div"));
	
	elems.canvas_cont.append(elems.canvas).appendTo(page)
	elems.page_options.append(elems.html_options).appendTo(page);
	
	
	/* The menu bar */
	elems.menu = $(document.createElement("div")).addClass(_cl("menu"));
	elems.uppermenu = $(document.createElement("div")).addClass(_cl("uppermenu"));
	elems.lowermenu = $(document.createElement("div")).addClass(_cl("lowermenu"));
	elems.menu.append(elems.uppermenu).append(elems.lowermenu);
	
	/* Command line */
	elems.commandline = $(document.createElement("input")).attr({'type':'text','name':'commandline'});
	
	/* Dates. Position inside a div */
	elems.dates = $(document.createElement("div")).addClass(_cl("dateholder"));
	elems.start = $(document.createElement("input")).attr({'type':'text','name':'start'}).addClass(options.inputDateClass);
	elems.end   = $(document.createElement("input")).attr({'type':'text','name':'end'}).addClass(options.inputDateClass);
	$.ecoplot.set_default_dates($this);
	
	if(options.commandline.periodlabel) {
		elems.dates.append($(document.createElement("label")).html(options.commandline.periodlabel+''));
	}
	elems.dates.append(elems.start);
	elems.dates.append($(document.createElement("span")).html(' - '));
	elems.dates.append(elems.end);
	
	/* Create the navigation menu */
	elems.nav_menu    = $(document.createElement("div")).addClass(_cl("nav-menu"));
	nav_menu_ul = $(document.createElement("ul"));
	elems.nav_menu.append(nav_menu_ul);
	elems.actionsmenu = nav_menu_ul;
	
	var disp = 'none';
	if(options.caneditchart) {
		disp = 'inline';
		_option_html(elems.html_options);
	}
	nav_menu_ul.append($(document.createElement("li"))
			.css({'list-style-type': 'none','display':disp}).append(
		   $(document.createElement("a"))
		   .attr({'title':'Edit chart'}).addClass('edit-chart').html('edit')));
	
	elems.uppermenu.append(elems.commandline);
	elems.lowermenu.append(elems.dates).append(elems.nav_menu).append(elems.loader);
	
	var cmdlin = options.commandline;
	if(cmdlin.symbol)  {
		elems.commandline.val(cmdlin.symbol+'');
	}
	if(!cmdlin.show) {
		elems.uppermenu.css({'display':'none'});
	}
	
	$this.append(elems.menu);
	$this.append(page);
	options.height = Math.max($this.height() - elems.menu.height() - 10,20);
} 

})(jQuery);