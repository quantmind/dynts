/* 
 * Econometric Ploting Plugin for jQuery
 * 
 * version: 0.4
 * 
 * @requires jQuery v1.4 or Later
 * @requires jQuery-UI v1.8 or Later
 * @requires Flot v0.6 or Later
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
    
    $('.ploting-elems').ecoplot(options);
    
    options is an object containing several input parameters. All parameters
    have sensible default values apart from one which
    needs to supplied.
      
      load_url: String for the remote data provider URL.
    
    The most common options are:
    
    	* flot_options: Object containing Flot-specific options
    	* dates: Object for specifying how dates are displayed
*/

$.extend({
	ecoplot: new function() {
		var extraTools     = {};
		var events         = {};
		var menubar		   = {};
		var debug		   = false;
		var css_loaded	   = false;
		var siteoptions	   = {
			url: null,
			theme: 'smooth'
		};
		
		var default_command_line = {
		    css:		 null,
		    show:		 true,
		    symbol:	 	 null,
		};
		
		var showPannel = function(p,el) {
			$('.secondary .pannel').hide();
			el.options.elems.body.addClass('with-pannel');
			if(p) {
				p.show();
			}
			c = el.options.canvases;
			if(c) {
				if(c.render()) {
					p.html('').append(c.current.edit);
				}
			}
		}
		var hidePannel = function(p,el) {
			$('.secondary .pannel').hide();
			el.options.elems.body.removeClass('with-pannel');
			if(el.options.canvases) {
				el.options.canvases.render();
			}
		}
		
		var default_toolbar = [
		        {
					classname: 'zoomout',
					title: "Zoom Out",
					icon: "ui-icon-zoomout",
					decorate: function(b,el) {
						b.click(function(e) {
							var pl = el.options.canvases;
							if(pl) {
								pl.render();
							}
						});
		        	}
				},
				{
					classname: 'reload',
					title: "Refresh data",
					icon: "ui-icon-refresh",
					decorate: function(b,el) {
						var $this = $(el);
						b.click(function(e) {
							$this.trigger('pre-reload',[this, $this]);
							$.ecoplot.loadData($this);
						});
					}
				},
				{
					classname: 'options',
					title: "Edit plotting options",
					icon: "ui-icon-image",
					type: "checkbox",
					decorate: function(b,el) {
						var options = el.options.elems.options;
						b.toggle(
								function() {showPannel(options,el);},
								function() {hidePannel(options,el);}
						);
					}
				}
				]
		
		this.siteoptions = siteoptions;
		
		this.defaults = {
			responcetype:   'json',
			requestMethod:  'get',
			elems:			{},
			dates:			{
				show: true,
				label: 'Period',
				format: "d M yy",
				cn: "ts-input-date"
					},
			command:		{show: true, entry: null},
			toolbar:		default_toolbar,
			commandline:	default_command_line,
			requestParams: 	{},
			show_tooltip:	true,
		    autoload:		true,
		    load_url:		null,
		    loaderimage:	'ajax-loader.gif',
		    flot_options:	{
							xaxis: {}
							},
		    paginate:		null,
		    infoPanel:		'ecoplot-info',
		    defaultFade:	300,
		    actions:		 ['zoom', 'datepicker', 'tooltip'],
		    default_month_interval: 12,
		    classname:		 'ts-plot-module',
		    errorClass:		 'dataErrorMessage',
		    canvasClass:	 'ts-plot-module-canvas',
		    convasContClass: 'ts-plot-module-canvas-container',
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
					console.log('$.ecoplot: '+ s);
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
		
		/**
		 * Set default dates in the date pannel.
		 */
		function _set_default_dates($this)  {
			var options = $this[0].options;
			var dates = options.dates;
	    	var td = new Date();
	    	var v2 = $.datepicker.formatDate(dates.format, td);
	    	td.setMonth(td.getMonth() - options.default_month_interval);
	    	var v1 = $.datepicker.formatDate(dates.format, td);
	    	dates.start.val(v1);
	    	dates.end.val(v2);
	    }
		
		/**
		 * For loading css. Not used yet.
		 */
		function loadCss() {
			if(siteoptions.url) {
				var theme = siteoptions.theme + '.css';
				var head = $(head);
				var link1 = $(document.createElement('link'));
				var link2 = $(document.createElement('link'));
				link1.css({type: "text/css",
					 	   rel: "stylesheet",
				 		   href: url + '/ecoplot/ecoplot.css'});
				link2.css({type: "text/css",
				 	   	   rel: "stylesheet",
			 		       href: url + '/ecoplot/skins/' + theme});
				head.append(link1);
				head.append(link2);
			}
		}
		
		/**
		 * Register ecoplot events
		 */
		function _registerEvents($this) {
			var opt = $this[0].options
			var elems = opt.elems;
			
			$(window).resize(function() {
				if(opt.canvases) {
					opt.canvases.render();
				}
	        });
			
			var actions = $this[0].options.actions;
			$.each(actions, function(i,v) {
				var eve = events[v];
				if(eve) {
					log('Registering event '+v);
					eve.register($this);
				}
    		});
    	}
		
		function _get_data($this)  {
			var opt = $this[0].options;
			var ticker = opt.elems.commandline.val()
			if(!ticker) {return null;}
			return {
				start: opt.dates.start.val(),
				end: opt.dates.end.val(),
				period:'',
				command:ticker
			};
		}
		
		/**
		 * Create the editing pannel for data
		 */
		function _editpannel(data) {
			var table = $('<table class="plot-options"></table>');
			var head = $('<tr></tr>').appendTo($('<thead></thead>').appendTo(table));
			head.html('<th>serie</th><th>show</th><th>ax1</th><th>ax2</th><th>line</th><th>points</th>');
			var body = $('<tbody></tbody>').appendTo(table);
			var tdinp = function (type,name,value,checked) {
				var check = $('<input type="'+type+'" name="'+name+'" value="'+value+'">');
				if(checked) {
					check.attr('checked',true);
				}
				return $('<td class="center"></td>').append(check);
			}
			$.each(data.series, function(i,serie) {
				var tr = $('<tr class="serie-option"></tr>').appendTo(body);
				tr.append($('<td>'+serie.label+'</td>'));
				tr.append(tdinp('checkbox','show','show',i<=1));
				tr.append(tdinp('radio','axis'+i,'ax1',serie.xaxis ? serie.xaxis==1 : i==0));
				tr.append(tdinp('radio','axis'+i,'ax2',serie.xaxis ? serie.xaxis==2 : i>0));
				tr.append(tdinp('checkbox','line','line', serie.lines ? serie.lines.show : true));
				tr.append(tdinp('checkbox','points','points', serie.points ? serie.points.show : false));
			});
			table.click(function() {
				data.render();
			});
			return table;
		}
		
		/**
		 * Internal function for creating a Flot canvas
		 */
		function _add(options, el_, data_) {
			el_.addClass(options.canvasClass);
			var typ = data_.type;
			log('Adding '+ typ + ' data to flot canvases.');
			
			var renderflot = function(height,opts) {
				var zoptions;
				if(opts) {zoptions = $.extend(true, {}, this.options, opts);}
				else {zoptions = this.options;}
				if(height) {
					this.height = height;
				}
				this.elem.height(this.height);
				var adata = [];
				var series = this.series;
				this.edit.find('tr.serie-option').each(function(i) {
					var el = $(this);
					if($("input[name='show']",el).attr('checked')) {
						var serie = series[i];
						if($("input[value='ax1']",el).attr("checked")) {
							serie.yaxis = 1;
						}
						else {
							serie.yaxis = 2;
						}
						adata.push(serie);
					}
				});
				this.flot = $.plot(this.elem, adata, zoptions);
				return this;
			}
			
			data_.elem = el_;
			data_.render = renderflot;
			data_.options = $.extend(true, {}, options.flot_options);
			data_.edit = _editpannel(data_);
			if(typ == 'timeseries') {
				data_.options.xaxis.mode = 'time';
			}
			else {
				data_.options.xaxis.mode = null;
			}
			return data_;
		}
		
		/**
		 * Internal function for rendering flot
		 */
		var _render = function(idx,opts) {
			var all = this.all;
			if(all.length > 0) {
				var c = this.current;
				if(idx!=undefined && idx>=0 && idx < all.length) {
					c = all[idx];
				}
				if(c != this.current) {
					//if(this.current) {
					//	this.current.hide();
					//}
					this.current = c;
				}
				c.render(this.height,opts);
				return true;
			}
			else {
				return false;
			}
		}
		
		/**
		 * Internal function for setting up one or more flot plot depending on data.
		 * It creates the options.canvases object of the form:
		 * 
		 * options.canvases = {
		 * 			all: Array of canvases
		 * 			height: height of canvas
		 * 			current: index of current canvas or null
		 * 			}
		 */
		function _set_new_canavases($this,data) {
			var options = $this[0].options;
			var container = options.elems.canvas_cont;
			container.children().fadeOut(options.defaultFade).remove();
			var outer = $('<div></div>').appendTo(container).height(container.height());
			var datac,typ;
			options.canvases = {current: null, render: _render};
			canvases = [];
			options.canvases.all = canvases; 
			
			if(data) {
				if(data.length == 1) {
					canvases.push(_add(options,outer,data[0]));
				}
				/* Setup tabs if data has more than one plot*/
				else {
					/* Setup tabs */
					var cid, cv
					var ul = $('<ul></ul>').appendTo(outer);
					$.each(data, function(i,v) {
						cid = 'canvas' + i;
						ul.append($('<li><a href="#' + cid + '">' + v.name + '</a></li>'));
						cv  = $('<div></div>').attr('id',cid);
						outer.append(cv);
						canvases.push(_add(options,cv,v));
					});
					outer.tabs({
						show: function(event,ui) {
							if(options.canvases.height) {
								options.canvases.render(ui.index);
							}
						}
					}); 
				}
			}
			options.canvases.height = outer.height()- $('ul',outer).height();
			options.canvases.render(0);
		}
		
		/**
		 * Render data.
		 * @param $this, the ecoplot element
		 * @param data, Array of plot canvases
		 * 
		 * }
		 */
		function _finaliseLoad($this,data) {
			var options = $this[0].options
			var elems = options.elems;
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
	 		var options  = $this[0].options;
	 		if(!options.load_url)  {return;}
	 		var dataplot = _get_data($this);
	 		if(!dataplot) {return;}
	 		log("Sending ajax request to " + options.load_url);
	 		log(dataplot.command + ' from ' + dataplot.start + ' end '+ dataplot.end);
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
		 * The constructor
		 */
		function _construct(options_) {
			return this.each(function(i) {
				var options = _parseOptions(options_, $.ecoplot.defaults);
				var $this = $(this).attr({'id':options.classname+"_"+i});
				this.options = options;
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
				$this.fadeIn(options.defaultFade);
				if(options.layout) {
					options.layout($this);
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
		
		this.addMenu = function(menu) {
			menubar[menu.name] = menu;
		}
		this.getmenu = function(name,$this) {
			var menu = menubar[name];
			if(menu) {
				return menu.create($this[0]);
			}
		}
	}
});



$.fn.extend({
    ecoplot: $.ecoplot.construct
});



var ecop = $.ecoplot;


///////////////////////////////////////////////////
//	SOME ACTIONS
///////////////////////////////////////////////////
$.ecoplot.addEvent({
	id: 'zoom',
	className: 'zoom-out',
	register: function($this) {
		var comm;
		var options = $this[0].options;
		$this.bind("plotselected", function (event, ranges) {
			var canvases = options.canvases;
			if(!canvases) {
				return;
			}
			pl = canvases.current;
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
            pl.render(canvases.height,opts);
            // don't fire event on the overview to prevent eternal loop
            //overview.setSelection(ranges, true);
    	});
	}
});


ecop.addEvent({
	id: 'datepicker',
	register: function($this) {
		var options = $this[0].options.dates;
		$('.'+options.cn,$this).datepicker({
			defaultDate: +0,
			showStatus: true,
			beforeShowDay: $.datepicker.noWeekends,
			dateFormat: options.format, 
		    firstDay: 1, 
		    changeFirstDay: false
		    //statusForDate: highlightToday, 
		    //showOn: "both", 
		    //buttonImage: prosp._classConfig.media_files_url + "img/icons/calendar_edit.png",
		    //buttonImageOnly: true
		});
	}
});


ecop.addEvent({
	id: 'tooltip',
	register: function($this) {
		var options = $this[0].options;
		var cl = 'econometric-plot-tooltip';
		function showTooltip(x, y, contents) {
	        $('<div class="'+cl+'">' + contents + '</div>').css( {
	            position: 'absolute',
	            display: 'none',
	            top: y + 5,
	            left: x + 5,
	        }).appendTo("body").fadeIn(200);
	    }
		
		$this.bind("plothover", function (event, pos, item) {
	        $("#x").text(pos.x.toFixed(2));
	        $("#y").text(pos.y.toFixed(2));

	        if(options.show_tooltip) {
	        	var canvas = options.canvases.current;
	            if (item) {
	                if (previousPoint != item.datapoint) {
	                    previousPoint = item.datapoint;
	                    
	                    $("."+cl).remove();
	                    var x = item.datapoint[0].toFixed(2),
	                        y = item.datapoint[1].toFixed(2);
	                    if(canvas.type == 'timeseries') {
	                    	x = new Date(parseFloat(x));
	                    	x = $.datepicker.formatDate(options.dates.format, x);
	                    }
	                    
	                    showTooltip(item.pageX, item.pageY,
	                                item.series.label + " of " + x + " = " + y);
	                }
	            }
	            else {
	                $("."+cl).remove();
	                previousPoint = null;            
	            }
	        }
	    });

	}
});


/////////////////////////////////////////////////////////////
//	MENUBAR
/////////////////////////////////////////////////////////////

/**
 * Add Command Input
 */
$.ecoplot.addMenu({
	name: 'command',
	classname: 'command',
	create: function(elem) {
		var command = elem.options.command;
		var el = $('<input type="text" name="commandline">');
		if(!command.show) {
			el.hide();
		}
		return el;
	}
});

/**
 * Add Date inputs menu creator
 */
$.ecoplot.addMenu({
	name: 'dates',
	classname: 'dateholder',
	create: function(elem) {
		var dates = elem.options.dates;
		var el = $('<div class="'+ this.classname + ' menu-item"></div>');
		var start_id = elem.id+'_start';
		var end_id = elem.id+'_end';
		if(dates.label) {
			el.append($('<label for_id="'+start_id+'">'+dates.label+'</label>'));
		}
		dates.start = $('<input id="'+start_id+'" class="'+dates.cn+'" type="text" name="start">');
		dates.end   = $('<input id="'+end_id+'" class="'+dates.cn+'" type="text" name="end">');
		el.append(dates.start);
		el.append($('<label class="middle">-</label>'));
		el.append(dates.end);
		if(!dates.show) {
			el.hide();
		}
		return el;
	}
});


/**
 * Add Toolbar items as specified in the options.toolbar array.
 */
$.ecoplot.addMenu({
	name: 'toolbar',
	classname: 'toolbar',
	create: function(elem) {
		var toolbar = elem.options.toolbar;
		var el = $('<div class="'+ this.classname + ' menu-item"></div>');
		var id = elem.id+'_'+this.classname;
		var sl = $('<span id="'+id+'"></span>').appendTo(el);
		$.each(toolbar, function(i,el) {
			id = elem.id+'_'+el.classname;
			var tel = null, eel = null;
			var ico;
			if(!el.type || el.type == 'button') {
				tel = $('<button id="'+id+'" class="'+el.classname+'">'+el.title+'</button>');
			}
			else if(el.type == 'checkbox') {
				tel = $('<input id="'+id+'" type="checkbox" class="'+el.classname+'"/>');
				eel = $('<label for="'+id+'">'+el.title+'</label>');
			}
			if(tel) {
				sl.append(tel);
				if(eel) {
					sl.append(eel);
				}
				ico = {};
				if(el.icon) {
					ico.primary = el.icon;  
				}
				tel.button({
					text: el.text || false,
					icons: ico
				});
				if(el.decorate) {
					el.decorate(tel,elem);
				}
			}
		});
		return el;
	}
});


///////////////////////////////////////////////////
//		DEFAULT PAGINATION
//		This can be overritten
///////////////////////////////////////////////////
$.ecoplot.paginate = function($this) {
	var options = $this[0].options;
	var elems   = options.elems;
	
	elems.menu = $('<div class="menu"></div>').appendTo($this);
	elems.body = $('<div class="body"></div>').appendTo($this);
	var page  = $('<div class="main"></div>').appendTo(elems.body);
	var page2 = $('<div class="secondary"></div>').appendTo(elems.body);
	
	elems.canvas_cont  = $('<div class="canvas-container"></div>').appendTo(page);
	elems.options = $('<div class="pannel options"></div>').appendTo(page2);
	elems.logger  = $('<div class="pannel logger"></div>').appendTo(page2);
	elems.loader  = $('<div class="loader"></div>');
	
	/* The menu bar */
	var upperm = $('<div class="uppermenu"></div>');
	var lowerm = $('<div class="lowermenu"></div>');
	elems.menu.append(upperm).append(lowerm);
	
	elems.commandline = $.ecoplot.getmenu('command',$this).appendTo(upperm);
	elems.dates = $.ecoplot.getmenu('dates',$this).appendTo(lowerm);
	lowerm.append($.ecoplot.getmenu('toolbar',$this));
	lowerm.append(elems.loader);
	
	var cmdlin = options.commandline;
	if(cmdlin.symbol)  {
		elems.commandline.val(cmdlin.symbol+'');
	}
	if(!cmdlin.show) {
		upperm.hide();
	}
	$.ecoplot.set_default_dates($this);
	options.layout = function(el) {
		elems = el[0].options.elems;
		var h = Math.max(el.height() - elems.menu.height(),30);
		elems.body.height(h);
		elems.canvas_cont.height(h-10).css({'margin':'5px 0'});
		el.height('auto');
	}
} 

})(jQuery);
