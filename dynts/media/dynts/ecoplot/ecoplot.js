/* 
 * Econometric Ploting JavaScript Library version @VERSION
 * 
 * @requires jQuery v1.6.1 or Later
 * @requires jQuery-UI v1.8 or Later
 * @requires Flot v0.7 or Later
 * 
 * Date: @DATE
 *
 */
/*
Flot plugin for automatically redrawing plots when the placeholder
size changes, e.g. on window resizes.

It works by listening for changes on the placeholder div (through the
jQuery resize event plugin) - if the size changes, it will redraw the
plot.

There are no options. If you need to disable the plugin for some
plots, you can just fix the size of their placeholders.
*/


/* Inline dependency: 
 * jQuery resize event - v1.1 - 3/14/2010
 * http://benalman.com/projects/jquery-resize-plugin/
 */
(function($,h,c){var a=$([]),e=$.resize=$.extend($.resize,{}),i,k="setTimeout",j="resize",d=j+"-special-event",b="delay",f="throttleWindow";e[b]=250;e[f]=true;$.event.special[j]={setup:function(){if(!e[f]&&this[k]){return false}var l=$(this);a=a.add(l);$.data(this,d,{w:l.width(),h:l.height()});if(a.length===1){g()}},teardown:function(){if(!e[f]&&this[k]){return false}var l=$(this);a=a.not(l);l.removeData(d);if(!a.length){clearTimeout(i)}},add:function(l){if(!e[f]&&this[k]){return false}var n;function m(s,o,p){var q=$(this),r=$.data(this,d);r.w=o!==c?o:q.width();r.h=p!==c?p:q.height();n.apply(this,arguments)}if($.isFunction(l)){n=l;return m}else{n=l.handler;l.handler=m}}};function g(){i=h[k](function(){a.each(function(){var n=$(this),m=n.width(),l=n.height(),o=$.data(this,d);if(m!==o.w||l!==o.h){n.trigger(j,[o.w=m,o.h=l])}});g()},e[b])}})(jQuery,this);


/* global jQuery */
(function ($) {

    $.isnothing = function (o) {
        return o === null || o === undefined;
    };
    $.selector_from_class = function(cl) {
        var c = '';
        $.each(cl.split(' '),function(i,v) {
            c+='.'+v;
        });
        return c;
    };
    
    /*
	 * Usage Note: -----------
	 * 
	 * $('.ploting-elems').ecoplot(options);
	 * 
	 * options is an object containing several input parameters. All parameters
	 * have sensible default values apart from one which needs to supplied.
	 * 
	 * url: String for the remote data provider URL.
	 * 
	 * The most common options are:
	 * 
	 * flot_options: Object containing Flot-specific options dates: Object for
	 * specifying how dates are displayed
	 */    
    $.ecoplot = (function () {
        
        function console_logger(msg) {
            if (typeof console !== "undefined" && typeof console.debug !== "undefined") {
                console.log(msg);
            }
        }
        
        var version = "0.4.2",
            authors = 'Luca Sbardella',
            home_page = 'https://github.com/quantmind/dynts',
            plugin_class = "econometric-plot",
            idkey = 'ecoplot_instance_id',
            instances = [],
            plugins = {},
            extraTools = {},
            menubar = {},
            debug = false,
            default_logger = {
                log: function (msg,level) {console_logger(msg);},
                info : function (msg) {console_logger(msg);},
                debug : function (msg) {console_logger(msg);},
                error : function (msg) {console_logger(msg);}                
            },
            tools = {
                  'legend': {
                               classname: 'toggle-legend',
                               title: "Toggle legend",
                               icon: "ui-icon-comment",
                               type: "checkbox",
                               decorate: function (b) {
                                   b.toggle(
                                           function () {
                                               var legend = $.ecoplot.instance(this).legend();
                                               if(legend) {
                                                   legend.hide();
                                               }
                                           },
                                           function () {
                                               var legend = $.ecoplot.instance(this).legend();
                                               if(legend) {
                                                   legend.show();
                                               }
                                           }
                                  );
                               }
                            }
            },
            defaults = {
               showplot: function (i) {return true;},
               show_tooltip: true,
               plugins: [],
               flot_options: {
                   xaxis: {},
                   legend: {
                       show:true,
                       position: "ne"
                       },
                   grid: {
                       show: true
                   }
               },
               infoPanel: 'ecoplot-info',
               min_height: 200,
               defaultFade: 300,
               classname: 'ts-plot-module',
               errorClass: 'dataErrorMessage',
               styling: 'jquery-ui'
           };
        
        
        // /////////////////////////////////////////////////////
        // DEFAULT PAGINATION
        //
        // To override create a plugin with paginate function.
        // /////////////////////////////////////////////////////
        function _set_dimensions(instance) {
        	var options = instance.settings(),
        		data = instance.data,
                container = instance.container().show(),
                height = container.height(),
                h;

            if(height < 10) {
                height = options.height || options.min_height;
            }
            h = Math.max(height - data.menu.container.height(),30);
            data.canvases.body.height(h);
            instance.canvas_container().height(h-10).css({'margin':'5px 0'});
            container.height('auto');
        }
           
        function _addelement(el,holder) {
            var id  = el.id.toLowerCase();
            var p   = holder[id];
            if(!p) {
                el.id = id;
                holder[id] = el;
            }
        }

        function _parseOptions(options_) {
            var options = {};
            $.extend(true, options, defaults, options_);
            return options;
        }
        
        function make_instance(index_, container_, settings_) {
        	var _layouts = [],
        		_inputs = [],
        		instance = {
	                data: {},
	                settings: function () { return settings_; },
	                index: function () { return index_; },
	                container: function () { return container_; },
	                paginate: function() {
	                	container_.hide().html("");
	                	$.each(_layouts, function(i,layout) {
	                		layout();
	                	});
	                	_set_dimensions(this);
	                	container_.trigger('ecoplot-ready',instance);
	                },
	                input_data: function() {
	                	var d = {}
	                	$.each(_inputs,function(i,inp) {
	                		$.extend(d,inp());
	                	});
	                	return d;
	                }
            	};
        	
        	function make_function (fname,func) {
                if(fname.charAt(0) == '_') {
                    return func;
                }
                else {
                    return function () {
                        var container = this.container(),
                            args = Array.prototype.slice.call(arguments),
                            res;
                        container.trigger('ecoplot-before-'+fname,args);
                        res = func.apply(this,args);
                        container.trigger('ecoplot-after-'+fname,res);
                        return res;
                    };
                }
            }
        	
        	// Add plugins
            $.each(settings_.plugins, function (i,name) {
                var extension = plugins[name];
                if(extension) {
                	$.ecoplot.log.debug('Processing plugin '+name+' on instance '+index_);
                    instance.data[name] = $.extend({},extension.data || {});                    
                    $.each(extension,function (fname,elem) {
                        if(fname == 'init') {
                            elem.apply(instance);
                        }
                        else if(fname == 'layout') {
                        	_layouts.push($.proxy(elem,instance));
                        }
                        else if(fname == 'get_input_data') {
                        	_inputs.push($.proxy(elem,instance));
                        }
                        else if(fname !== 'data') {
                            if($.isFunction(elem)) {
                                elem = make_function (fname,elem);
                            }
                            instance[fname] = elem;
                        }
                    });
                }
            });
            
            return instance;
        }
        /**
		 * The jQuery plugin constructor
		 */
        function _construct(options_) {
            var options = _parseOptions(options_);
            
            // Loop over each element and initialize the jquery plugin.
            return this.each(function (i) {
                var $this = $(this),
                    instance_id = $this.data(idkey),
                    instance;
                if(typeof instance_id !== "undefined" && instances[instance_id]) {
                    instances[instance_id].destroy();
                }
                instance_id = parseInt(instances.push({}),10) - 1;
                $this.data(idkey,instance_id)
                     .attr({'id':plugin_class+"_"+instance_id})
                     .addClass(plugin_class);
                
                instance = instances[instance_id] = make_instance(
                        instance_id,$this, options);
                instance.paginate();
            });
        }


        // API FUNCTIONS AND PROPERTIES
        // ///////////////////////////////////////////////////////////////
        return {
            construct: _construct,
            removeEvent: function (id){delete events[id];},
            'defaults': defaults,
            button: function(text, icon) {
            	var el =  $('<button>'+text+'</button>').addClass('button');
            	return el.button();
            },
            debug: function (){return debug;},
            setdebug: function (v){debug = v;},
            count: function () {return instances.length;},
            instance: function (elem) {
                // get by instance id
                if(instances[elem]) { return instances[elem]; }
                var o = $(elem); 
                if(!o.length && typeof elem === "string") { o = $("#" + elem); }
                if(!o.length) { return null; }
                return instances[o.closest("."+plugin_class)
                                  .data(idkey)] || null;
            },
            log: default_logger,
            'version': version,
            info: function() {return {'version':version,
                                      'authors':authors,
                                      'home_page':home_page};},
            'plugin_class': plugin_class,
            addMenu: function (menu) {menubar[menu.name] = menu;},
            getmenu: function (name,$this) {
                var menu = menubar[name];
                if(menu) {
                    return menu.create($this[0]);
                }
            },
            tool: function (name) {
                return tools[name];
            },
            plugin: function (pname, pdata) {
                var tbs = pdata.tools || {};
                $.each(tbs, function (name,val) {
                    val.plugin = pname;
                    tools[name] = val;
                });
                defaults[pname] = pdata.defaults || {};
                plugins[pname] = pdata;
                if(pdata.isdefault) {
                    defaults.plugins.push(pname);
                }
            },
            resize: function () {
                $(window).trigger('resize');
            }
        };
    }());



    $.fn.extend({
        ecoplot: $.ecoplot.construct
    });
    

    // Resizing plugin for flot
    $.plot.plugins.push({
        options: {},
        name: 'resize',
        version: '1.0',
        init: function (plot) {
            function onResize() {
                var placeholder = plot.getPlaceholder(),
                    instance = $.ecoplot.instance(placeholder);
                // somebody might have hidden us and we can't plot
                // when we don't have the dimensions
                if (placeholder.width() === 0 || placeholder.height() === 0) {
                    return;
                }
                instance.container().trigger('ecoplot-pre-resize');
                plot.resize();
                plot.setupGrid();
                plot.draw();
            }
            
            function bindEvents(plot, eventHolder) {
                plot.getPlaceholder().resize(onResize);
            }

            function shutdown(plot, eventHolder) {
                plot.getPlaceholder().unbind("resize", onResize);
            }
            
            plot.hooks.bindEvents.push(bindEvents);
            plot.hooks.shutdown.push(shutdown);
        }
    });
    
    
    /*========================================================================
     * 
     * PLUGINS
     * An ecoplot plugin is created in the following way:
     * 
     * 
     * 		$.ecoplot.plugin(plugin_name,{
     * 								defaults : {...},
     * 								data: {...},
     * 								init: function() {...},
     * 								layout: function() {...}
     * 							});
     * 
     * 
     *  - data
     *  
     *  An object which is added to the instance.data object so that
     *  instance.data.plugin_name will contain its value.
     *  It can be used to store dynamic data for the plugin.
     *  
     *  - layout
     *  
     *  An optional function, which will be called, if availale, during the
     *  layout of the ecoplot instance.
     */
    
    
    /*================================================================
     * 
     * Menu plugin
     * 
     * 
     */
    $.ecoplot.plugin('menu',{
        isdefault: true,
    	defaults: {
    		container: null,
    		container_class: 'menu'
    	},
    	layout: function() {
    		var options = this.settings(),
    			omenu = options.menu,
    			menu = this.data.menu,
    			container = this.container(),
    			mc = $(omenu.container),
    			lower;
    		if(!mc.length) {
    			mc = $('<div></div>').appendTo(container);
    			menu.upper = $('<div class="menubar upper ui-widget-header"></div>').appendTo(mc).hide();
        		lower = $('<div class="lower ui-widget-header"></div>').appendTo(mc);
        		menu.lower = $('<div class="menubar"></div>').appendTo(lower);
        		lower.append($('<div></div>').addClass(options.jsondata.loader_class));
    		}
    		menu.container = mc.addClass(omenu.container_class);
    	}
    });
    
    // ////////////////////////////////////////////////////////////////////////////
    // Canvases plugin
    // This is the main plugin which adds the standard plotting functionalities
    // ////////////////////////////////////////////////////////////////////////////
    $.ecoplot.plugin('canvases',{
        isdefault: true,
        defaults : {
            legend_class: 'ecolegend ui-state-default',
            legend_padding: 5,
            legend_draggable: true,
            outer_body_class: 'body',
            container_class: 'canvas-container',
            canvas_class: 'ts-plot-module-canvas'
        },
        data: {
            all: [],
            current: null
        },
        init: function() {
            var instance = this,
            	opts = this.settings().canvases,
            	cdata = this.data.canvases;
            cdata.legend_selector = $.selector_from_class(opts.legend_class);
            this.container().bind('ecoplot-pre-resize',function() {
                var canvas = instance.get_canvas();
                $.ecoplot.log.debug('resizing canvas');
                instance._set_legend_position(canvas);
            }).bind('redraw', function(e, dataplot) {
            	var canvas = instance.get_canvas();
            	$.each(canvas, function(){
            		canvas.need_redraw = dataplot;
            	});
            	instance.get_canvas();
            });
        },
        layout: function() {
        	var options = this.settings(),
        		canvases = options.canvases,
				container = this.container(),
				cdata = this.data.canvases;
			cdata.body = $('<div class="ui-widget-content"></div>')
			 			.addClass(canvases.outer_body_class)
						.appendTo(container).height(options.height);
			cdata.main = $('<div class="main"></div>').appendTo(cdata.body);
			cdata.secondary = $('<div class="secondary"></div>').appendTo(cdata.body);
			cdata.canvas_container = $('<div></div>').addClass(canvases.container_class).appendTo(cdata.main);
        },
        height: function () {
            var c = this.canvas_container();
            return c.height() - $('ul',c).height();
        },
        get_canvas: function (idx) {
            var canvases = this.data.canvases;
            if($.isnothing(idx)) {
                idx = canvases.current;
            }
            if(!$.isnothing(idx)) {
                var canvas = canvases.all[idx];
                if(canvas) {
                	canvas.index = idx;
                	this.container().trigger('get_canvas', canvas);
                    return canvas;
                }
            }
        },
        canvas_container: function () {
        	return this.data.canvases.canvas_container;
        },
        _get_serie_data: function (idx,canvas) {
            return canvas.series;
        },
        // Render a canvas. If idx is null or undefined it renders the current
		// canvas
        canvas_render: function (idx, opts) {
            var instance = this,
                canvas = this.get_canvas(idx),
                options = canvas.options,
                container = this.canvas_container(),
                legend = canvas.options.legend.container,
                height,zoptions,adata,flot;
            if(!canvas) {return;}
            this.data.canvases.current = canvas.index;
            if(!legend) {
                var hooks = options.hooks || {},
                    hdraw = hooks.draw || [];
                legend = this.add_legend();
                options.legend.container = legend;
                hooks.draw = hdraw;
                hdraw.push(function(plot) {
                    instance._redraw_legend(plot);
                });
                options.hooks = hooks;
            }
            canvas.elem.height(this.height());
            if(opts) {
                this._set_legend_position(canvas,{});
                options = $.extend(true, {}, options, opts);
                canvas.flot = null;
            }
            adata = this._get_serie_data(canvas.index,canvas);
            flot = canvas.flot;
            if(!flot) {
                $.ecoplot.log.debug('Building flot object');
                canvas.flot = $.plot(canvas.elem, adata, options);
            }
            else {
                flot.setData(adata);
                flot.setupGrid();
                flot.draw();
            }
            return canvas;
        },
        // Add a new canvas to the list
        add_canvas: function (data, oldcanvas, outer) {
            var options = this.settings(),
                instance = this,
                $this = this.container(),
                canvases = this.data.canvases,
                typ = data.type,
                mtyp = typ == 'timeseries' ? 'time' : null,
                name = data.name,
                idx = canvases.all.length,
                cid = $this.attr('id') + '-canvas' + idx,
                foptions = $.extend(true, {}, options.flot_options, data.options),
                cv;
            
            if(!outer) {
                outer = $('div',this.canvas_container());
            }
            if(!idx) {
                $('<ul></ul>').appendTo(outer);
            }
            $('ul',outer).append($('<li><a href="#' + cid + '">' + name + '</a></li>'));
            
            if(oldcanvas && oldcanvas.options.xaxis.mode === mtyp) {
                var ole = oldcanvas.options.legend;
                this._set_legend_position(oldcanvas);
                oldcanvas.name = name;
                oldcanvas.oseries = oldcanvas.series; 
                oldcanvas.series = data.series;
                oldcanvas.flot = null;
                foptions = $.extend(foptions, oldcanvas.options);
                data = oldcanvas;
            }
            $.ecoplot.log.debug('Adding '+ typ + ' ' + name + ' to canvases.');
            cv = $('<div></div>').attr('id',cid)
                .addClass(options.canvases.canvas_class)
                .appendTo(outer);
            foptions.xaxis.mode = mtyp;
            data.options = foptions;
            data.elem = cv;
            canvases.all.push(data);
            return data;
        },
        // Replace all canvases with new ones
        replace_all_canvases: function (data) {
            var options = this.settings(),
                canvases = this.data.canvases,
                container = this.canvas_container(),
                outer = $("<div></div>").height(container.height()).hide(1),
                instance = this,
                oldouter = container.children().fadeOut(options.defaultFade),
                oldcanvases = canvases.all,
                datac,typ;
            canvases.all = [];
            
            function oldcanvas(c) {
                if(oldcanvases.length > c) {
                    return oldcanvases[c];
                }
            }

            if(data) {
                $.each(data, function (i,v) {
                    instance.add_canvas(v,oldcanvas(i),outer);
                });
                if(canvases.all.length === 1) {
                    $('ul',outer).remove();
                }
                oldouter.remove();
                container.append(outer);
                outer.show();
                if(canvases.all.length > 1) {
                    outer.tabs({
                        show: function (event,ui) {
                            instance.canvas_render(ui.index);
                        }
                    });
                }
            }
            if(!$.isnothing(canvases.current)) {
                if(canvases.current > canvases.all.length) {
                    canvases.current = 0;
                }
            } else {
                canvases.current = 0;
            }
            this.canvas_render();
        },
        add_legend: function () {
            var instance = this,
                options = this.settings().canvases,
                legend = $('<div></div>').addClass(options.legend_class)
                                         .css({position:'absolute',
                                               padding:options.legend_padding+'px'}).hide();
            return legend;
        },
        legend: function () {
            var canvas = this.get_canvas();
            if(canvas) {
                return canvas.options.legend.container;
            }
        },
        _set_legend_position: function (canvas, rpos) {
            if(canvas) {
                var legend = canvas.options.legend.container,
                    plot = canvas.flot;
                if(legend && plot) {
                    if(!rpos) {
                        var plotOffset = plot.getPlotOffset(),
                            w = plot.width() + plotOffset.right + plotOffset.left,
                            h = plot.height() + plotOffset.top + plotOffset.bottom,
                            p = legend.position();
                        rpos = {top:p.top/h,left:p.left/w};
                    }
                    canvas.options.legend.relative_position = rpos;
                }
            }
        },
        _redraw_legend: function (flot) {
            var options = this.settings().canvases,
                canvas = this.get_canvas(),
                legend = canvas.options.legend.container,
                rpos = canvas.options.legend.relative_position,
                plotOffset = flot.getPlotOffset(),
                opts = flot.getOptions(),
                c = flot.getPlaceholder(),
                lw,tw;
            if(!legend) {return;}
            $('td.legendColorBox',legend).css({'padding-right':'5px'});
            canvas.options.legend.relative_position = null;
            legend.appendTo(c);
            if(rpos) {
                if(!$.isnothing(rpos.left) && !$.isnothing(rpos.top)) {
                    var w = c.width(), h = c.height();
                    lw = Math.min(w - legend.width() - 2*options.legend_padding - 2,parseInt(rpos.left*w));
                    tw = Math.min(h - legend.height() - 2*options.legend_padding - 2,parseInt(rpos.top*h));
                    legend.css({left:lw,top:tw});
                }
            }
            else {
                var p = opts.legend.position,
                    m = opts.legend.margin;
                if (!$.isArray(m)) {
                    m = [m, m];
                }
                if (p.charAt(0) == "n") {
                    legend.css({top: (m[1] + plotOffset.top) + 'px'});
                }
                else if (p.charAt(0) == "s") {
                    legend.css({bottom: (m[1] + plotOffset.bottom) + 'px'});
                }
                if (p.charAt(1) == "e") {
                    lw = c.width() - legend.width() - plotOffset.right - m[0] - 2*options.legend_padding;
                    legend.css({left: lw + 'px'});
                }
                else if (p.charAt(1) == "w") {
                    legend.css({left: (m[0] + plotOffset.left) + 'px'});
                }
                legend.show();
            }
            if(options.legend_draggable) {
                legend.css({cursor:'move'}).draggable({containment:c});
            }
        }
    });
    

    // /////////////////////////////////////////////////
    // plugin for loading data via ajax
    // /////////////////////////////////////////////////
    $.ecoplot.plugin('jsondata',{
        isdefault: true,
        defaults: {
            autoload:true,
            responsetype: 'json',
            requestMethod: 'get',
            url: '.',
            errorcallbacks: [],
            requestparams: {},
            load_opacity: '0.7',
            loader_class: 'loader',
            data2body : null,
            parse: function (data,instance){return data;},
            startLoading: function (instance) {
                var options = instance.settings().jsondata;
                $('.'+options.loader_class,instance.container()).show();
                instance.canvas_container().css({'opacity':options.load_opacity});
            },
            stopLoading: function (instance) {
                var options = instance.settings().jsondata;
                $('.'+options.loader_class,instance.container()).css({'display':'none'});
                instance.canvas_container().css({'opacity':'1'});
            }
        },
        tools: {
            'reload': {
                        classname: 'reload',
                        title: "Refresh data",
                        icon: "ui-icon-refresh",
                        decorate: function (b, instance) {
                            b.click(function (e,o) {
                                var inst = $.ecoplot.instance(this);
                                instance.container().trigger('load');
                            });
                        }
                    }
        },
        init: function () {
            var self = this,
            	options = self.settings().jsondata,
            	container = self.container();
            self.data.jsondata.dataplot = null;
            container.bind('load', function() {
            	self.ajaxload();
            });
            if(options.autoload) {
                container.bind('ecoplot-ready', function () {
                	self.container().trigger('load');
                });
            }
        },
        ajaxdata: function () {
            var data = this.input_data();
            if(!data.command) {return;}
            return data;
        },
        ajaxload: function () {
            var options = this.settings().jsondata,
                log = $.ecoplot.log,
                instance = this,
                data = this.data.jsondata,
                load = true,
                dataplot;
            if(!options.url)  {return;}
            dataplot = this.ajaxdata();
            if(!dataplot) {return;}
            if(data.dataplot !== null) {
            	if(data.dataplot.command === dataplot.command) {
            		// The ticker has been already loaded
            		var start = new Date(data.dataplot.start),
            			data_start = new Date(dataplot.start),
            			end = new Date(data.dataplot.end),
            			data_end = new Date(dataplot.end);
            		if(start <= data_start && end >= data_end) {
            			load = false;
            			dataplot.start = data_start;
            			dataplot.end = data_end;
            		}
            	}
            }
            if(load) {
            	data.dataplot = dataplot;
	        	log.info("Sending ajax request to " + options.url);
	        	log.debug(dataplot.command + ' from ' + dataplot.start + ' end '+ dataplot.end);
	        	var params   = {
	        		timestamp: +new Date()
	        	};
	            $.each(options.requestparams, function (key, param) {
	                params[key] = typeof param === "function" ? param() : param;
	            });
	            params = $.extend(true, params, dataplot);
	            if (options.data2body) {
	            	params = options.data2body(params);
	            }
	            options.startLoading(this);
	            $.ajax({
	                url: options.url,
	                type: options.requestMethod,
	                data: params,
	                dataType: options.responsetype,
	                success: function (data) {
	                    log.info("Got the response from server");
	                    var pdata;
	                    try {
	                        pdata = options.parse(data, instance);
	                        if(!pdata) {
	                            log.error("Failed to parse.");
	                        }
	                    }
	                    catch(e) {
	                        log.error("Failed to parse. Error in line ",e);
	                    }
	                    options.stopLoading(instance);
	                    if(pdata)  {
	                        try {
	                            instance._ajaxdone(pdata);
	                        }
	                        catch(e2) {
	                            pdata = false;
	                            log.error("Failed after data has loaded",e2);
	                        }
	                    }
	                    if(!pdata) {
	                        $.each(options.errorcallbacks, function(i,f) {
	                            f(data,instance);
	                        });
	                    }
	                }
	            });
            }
            else {
            	this.container().trigger('redraw', dataplot);
            }
        },
        _ajaxdone: function (data) {
            this.replace_all_canvases(data);
        }
    });
    
    
    $.ecoplot.plugin('zoom',{
        isdefault: true,
        tools: {
                'zoomout': {
                            classname: 'zoomout',
                            title: "Zoom Out",
                            icon: "ui-icon-zoomout",
                            decorate: function (b) {
                                b.click(function (e) {
                                    var instance = $.ecoplot.instance(this);
                                    if(instance) {
                                        instance.canvas_render(null,{});
                                    }
                                });
                            }
                }
        },
        init: function () {
            this.data.zoom.selecting = false;
            this.container().bind('plotselected', function (event, ranges) {
                var instance = $.ecoplot.instance(this);
                instance.zoom(ranges);
            });
        },
        zoom: function (ranges) {
            var canvas = this.get_canvas(),
                opts = {},
                ax = canvas ? canvas.flot.getAxes() : null;
            if(!ax) {return;}
            function checkax(axis)  {
                if(axis.to - axis.from < 0.00001)  {
                    axis.to = axis.from + 0.00001;
                }
                return {min: axis.from, max: axis.to};
            }
            if(ax.xaxis && ranges.xaxis)  {
                opts.xaxis = checkax(ranges.xaxis);
            }
            if(ax.yaxis && ranges.yaxis)  {
                opts.yaxis = checkax(ranges.yaxis);
            }
            if(ax.x2axis && ranges.x2axis)  {
                opts.x2axis = checkax(ranges.x2axis);
            }
            if(ax.y2axis && ranges.y2axis)  {
                opts.y2axis = checkax(ranges.y2axis);
            }
            // do the zooming
            this.canvas_render(null, opts);
        }
    });
    
    
    $.ecoplot.plugin('dialog', {
        isdefault: true,
        dialog: function (title,body,opts) {
            var c = this.container(),
                d = $("<div></div>").appendTo(c).attr('title',title).html(body);
            d.dialog(opts).bind('dialogclose', function() {
                $(this).remove();
            }).dialog('open');
        }
    });
    
    $.ecoplot.plugin('image',{
        defaults: {
            title: 'Save as image',
            formats: ['png','jpeg','bmp']
        },
        tools: {
            'saveimage': {
                           classname: 'save-image',
                           title: "Save as image",
                           icon: "ui-icon-image",
                           decorate: function (b,el) {
                               b.click(function () {
                                   var instance = $.ecoplot.instance(this),
                                       body = instance.saveimagehtml(),
                                       opts = {
                                	   	   width: 'auto',
                                	   	   height: 'auto',
                                           buttons: {
                                               'Preview': function() {
                                                   var d = $(this),
                                                       xdim = $('input[name="scalex"]').val(),
                                                       ydim = $('input[name="scaley"]').val(),
                                                       as = $('select[name="format"]').val(),
                                                       preview = $('.preview',d),
                                                       img;
                                                   try {
                                                       xdim = parseInt(xdim,10);
                                                       ydim = parseInt(ydim,10);
                                                   }
                                                   catch(e) {
                                                       xdim=0;ydim=0;
                                                   }
                                                   img = instance.saveimage(as,xdim,ydim);
                                                   if(!preview.length) {
                                                       preview = $('<div class="preview"></div>').css({'margin':'10px 0'}).insertAfter($('form',d));
                                                   }
                                                   preview.html(img);
                                                },
                                                'Cancel': function() {
                                                    $( this ).dialog( "close" );
                                                }
                                           }
                                       };
                                   instance.dialog('Save as image',body,opts);
                                   // plot.saveAsPng();
                               });
                           }
                          }
        },
        init: function() {
            var fopts = this.settings().flot_options,
                grid  = fopts.grid || {};
            fopts.grid = grid;
            if(grid.show) {
                if(!grid.canvasText) {
                    grid.canvasText = {};
                }
                grid.canvasText.show = true;
            }
        },
        saveimagehtml: function() {
            var options = '',
                options = this.settings().image;
            $.each(options.formats,function(i,v) {
                options += '<option value="'+v+'">'+v+'</option>';
            });
            return "<form>"+
            "<label for='scalex'>X dimension</label><input name='scalex' value=''/><br />"+
            "<label for='scaley'>Y dimension</label><input name='scaley' value=''/><br />"+
            "<label for='format'>format</label><select name='format'>"+options+"</select>"+
            "</form>";
        },
        saveimage: function (strType, xdim, ydim) {
            var target = this.get_canvas(),
                canvas,oImg;
            
            if(!target) {return;}

            canvas = target.flot.getCanvas();
            if(strType == 'png') {
                oImg = Canvas2Image.saveAsPNG(canvas, true, xdim, ydim);
            }
            else if (strType == "bmp") {
                oImg = Canvas2Image.saveAsBMP(canvas, true, xdim, ydim);
            }
            else if (strType == "jpeg") {
                oImg = Canvas2Image.saveAsJPEG(canvas, true, xdim, ydim);
            }
            if (!oImg) {
                alert("Sorry, this browser is not capable of saving " + strType + " files!");
                return false;
            }
            return oImg;
        }
    });
    
    
    /*
	 * =================================================================
	 * EDIT plugin - Plugin for editing series
	 * 
	 * To customize pass the edit dictionary in the ecoplot options
	 * 
	 * $(#myplot).ecoplot({..., edit: {popup: true, ...} });
	 * 
	 * Options:
	 * 
	 * container: the html container of the options panel. Default null popup:
	 * If true a jquery dialog will be used to display options
	 * 
	 * 
	 * 
	 */
    
    $.ecoplot.plugin('edit',{
        isdefault: true,
        defaults: {
            editing_class: 'with-panel',
            container: null,
            container_class: 'panel-options',
            panel_class: 'panel',
            popup: false,
            title: 'Series options',
            autoredraw: true,
            render_as: 'table',
            headers: ['line','points','bars','shadow','fill','y-axis']
        },
        data: {
            headers: {
                yaxis1: {
                    label: 'y-axis1'
                },
                yaxis2: {
                    label: 'y-axis2'
                }
            }
        },
        tools: {
            edit: {
                classname: 'options',
                title: "Edit plotting options",
                icon: "ui-icon-copy",
                type: "checkbox",
                decorate: function (b,instance) {
                	var edit = instance.data.edit;
                    b.click(function() {
                    	if(b.prop('checked')) {
                    		instance.showPanel();
                    	}
                    	else {
                    		instance.hidePanel();
                    	}
                    });
                    instance.container().bind('close-edit-options', function() {
                    	if(b.attr('checked')) {
                    		b.prop('checked',false).button('refresh');
                    	}
                    });
                }
            }
        },
        init: function () {
            var options = this.settings().edit,
                instance = this;
            this.data.edit.panel_selector = $.selector_from_class(options.panel_class);
            this.container().bind('ecoplot-after-add_canvas', function (event, canvas, oldcanvas) {
                var instance = $.ecoplot.instance(this);
                instance.create_edit_panel(canvas,oldcanvas);
            }).bind('ecoplot-after-canvas_render', function (e) {
                if(instance.data.edit.isactive()) {
                    instance.showPanel();
                }
            });
        },
        layout: function() {
        	var instance = this,
        		options = this.settings().edit,
        		edit = this.data.edit,
        		c = $(options.container);
        		in_canvas = true;
        		
        	if(!c.length) {
        		in_canvas = true;
        		c = $('<div></div>').appendTo(this.data.canvases.secondary);
        	}
        	edit.container = c.addClass(edit.container_class);
        	
        	if(options.popup) {
        		var position = options.popup.position || ['right','top'];
        		c = c.dialog({title:options.title,
        					'position':position,
        					width:'auto',
        					height:'auto',
        					autoOpen:false,
        					close: function(e,ui) {
        						instance.container().trigger('close-edit-options');
        						//if(e.originalEvent) {
        					//		instance.container().trigger('close-edit-options');
        						//}
        					}});
        		edit.show = function() {this.container.dialog("open");};
        		edit.hide = function() {this.container.dialog("close");};
        		edit.isactive = function() {return this.container.dialog('isOpen');};
        	}
        	else if(in_canvas) {
        		edit.show = function() {
    				instance.data.canvases.body.addClass(options.editing_class);
    				this.container.show();
        		}
        		edit.hide = function() {
    				instance.data.canvases.body.removeClass(options.editing_class);
    				this.container.hide();
        		}
        		edit.isactive = function() {
        			return instance.data.canvases.body.hasClass(options.editing_class);
        		}
        	}
        	else {
        		edit.show = function(){};
        		edit.hide = function(){};
        		edit.isactive = function(){return true;};
        	}
        },
        showPanel: function (idx) {
            var canvas = this.get_canvas(idx),
                options = this.settings().edit,
                edit = this.data.edit;
            if(canvas) {
            	this.edit_panel().hide();
            	this.edit_panel(canvas.index).show();
            	edit.show();
            }
        },
        hidePanel: function () {
        	var edit = this.data.edit;
        	edit.hide();
        },
        //
        // Get the series editing panel
        edit_panel: function(idx,create) {
        	var edit = this.data.edit,
        		options = this.settings().edit;
        	if(!$.isnothing(idx)) {
	        	var cn = options.panel_class + ' option-' + idx;
	        		se = $.selector_from_class(cn),
	        		p = $(se,edit.container);
	        	if(!p.length && create) {
	        		p = $('<div class = "'+cn+'"></div>').appendTo(edit.container);
	        	}
	        	return p;
        	}
        	else {
        		return $($.selector_from_class(options.panel_class),edit.container);
        	}
        },
        //
        // Override the get serie data
        _get_serie_data: function (idx,canvas) {
            var adata = [];
            function show_elem(typ,el) {
                if($("input[name='"+typ+"']",el).attr('checked') ? true : false) {
                    var w = $("input[name='"+typ+"_width']",el);
                    if(w.length) {
                        w = w.val();
                        return w ? parseInt(w) || 1 : 0;
                    }
                    else {
                        return true;
                    }
                }
            }
            this.edit_panel(idx).find('tr.serie-option').each(function (i) {
                var el = $(this);
                var serie = canvas.series[i];
                serie.shadowSize = parseInt($("input[name='shadow']",el).val());
                serie.lines.lineWidth  = show_elem('line',el);
                serie.lines.show = serie.lines.lineWidth ? true : false;
                serie.points.radius = show_elem('points',el);
                serie.points.show = serie.points.radius ? true : false;
                serie.bars.barWidth = show_elem('bars',el);
                serie.bars.show = serie.bars.barWidth ? true : false;
                serie.lines.fill = show_elem('fill',el);
                if($("input[value='y-ax1']",el).attr("checked")) {
                    serie.yaxis = 1;
                }
                else {
                    serie.yaxis = 2;
                }
                if(serie.lines.show || serie.points.show || serie.bars.show) {
                    adata.push(serie);
                }
            });
            return adata;
        },
        // Create the editing panel
        create_edit_panel: function (canvas) {
            // check if oldcanvas is the same. If so keep it!
            var instance = this,
            	idx = this.data.canvases.all.length-1,
                options = this.settings(),
                edit = options.edit,
                data = this.data.edit,
                cn = 'option'+idx,
                body  = null,
                oldbody = null,
                oseries = [],
                showplot = options.showplot,
                edit_panel = this.edit_panel(idx,true),
                colspan = edit.headers.length,
                series_container;
            
            if(!edit_panel.length) {
                return;
            }
            
            if(!canvas.oseries) {
                $.ecoplot.log.debug('Creating editing panel.');
                edit_panel.children().remove();
                if(edit.autoredraw) {
                	edit_panel.data('ecoplot_instance',this.index());
                	edit_panel.change(function(e) {
                		var target = $(e.target);
                		if(target.is('input')) {
                			instance._set_legend_position(instance.get_canvas());
	                		instance.canvas_render();
                		}
                	});
                }
                else {
                	$('<h2>Series</h2>').css({'float':'left','margin':0}).appendTo(edit_panel);
                    $("<button>Redraw</button>").button().click(function() {
                        var instance = $.ecoplot.instance(this);
                        instance._set_legend_position(instance.get_canvas());
                        instance.canvas_render();
                    }).appendTo(edit_panel).css({'margin-left':'10px'});
                }
                if(edit.render_as === 'table') {
                	var head, head_val;
	                series_container = $('<table class="plot-options"></table>');
	                head = $('<tr></tr>').appendTo($('<thead class="ui-state-default"></thead>')
	                					 .appendTo(series_container));
	                head_val = '';
	                $.each(options.edit.headers, function() {
	                    var headdata = data.headers[this] || {},
	                        label = headdata.label || this;
	                    head_val+='<th class="center">'+label+'</th>';
	                });
	                head.html(head_val);
	                body = $('<tbody class="ui-widget-content"></tbody>').appendTo(series_container);
                }
                series_container.appendTo(edit_panel).css({'margin':'0 auto 20px'})
            }
            else {
                table = $('table',edit_panel);
                body = $('tbody',table).html('');
                oseries = canvas.oseries;
            }
            // Add a column element
            function makeinp(i,type,name,value,checked,label) {
            	var id = cn+'-'+name+'-serie'+i,
            		inp = $('<input id="'+id+'" type="'+type+'" name="'+name+'" value="'+value+'">');
            	if(checked) {
                    inp.prop({'checked':true});
                }
            	if(label) {
            		return $.merge(inp,$('<label for="'+id+'">'+label+'</label>'));
            	}
            	return inp;
            }
            
            function tdinp(i,type,name,value,tag,checked,w) {
                var inp = makeinp(i,type,name,value,checked);
                if(tag) {
                	tag = $('<'+tag+'></'+tag+'>').append(inp);
                }
                if(tag) {
                	if(w) {
                		return tag.append($('<input class="tiny" type="input" name="'+name+'_width" value="'+w+'">'));
                	}
                	return tag;
                }
                else {
                	return inp;
                }
            }
            
            function checkmedia(med,show) {
                if(med) {
                    if(med.show === undefined) {
                        med.show = show;
                    }
                }
                else {
                    med = {show: show};
                }
                return med;
            }
            
            $.each(canvas.series, function (i,serie) {
                var oserie = null,
                    shadow, radio;
                if(oseries.length > i) {
                    var os = oseries[i];
                    if(serie.label === os.label) {
                        oserie = os;
                    }
                }
                if(!oserie) {
                    serie.lines  = checkmedia(serie.lines,showplot(i));
                    serie.points = checkmedia(serie.points,false);
                    serie.bars   = checkmedia(serie.bars,false);
                    serie.color  = serie.color || i;
                }
                else {
                    serie.lines  = oserie.lines;
                    serie.points = oserie.points;
                    serie.bars   = oserie.bars;
                    serie.yaxis  = oserie.yaxis;
                    serie.xaxis  = oserie.xaxis;
                    serie.shadowSize = oserie.shadowSize;
                    serie.color  = $.isnothing(oserie.color) ? i : oserie.color;
                }
                shadow = serie.shadowSize || 0;
                shadow = $('<input class="tiny" type="input" name="shadow" value="'+ shadow +'">');
                var trt = $('<tr class="serie'+i+' serie-title"></tr>').appendTo(body);
                var tr  = $('<tr class="serie'+i+' serie-option"></tr>').appendTo(body);
                if(parseInt((i+1)/2)*2 === i+1) {
                    trt.addClass('ui-state-default').css('border','none');
                    tr.addClass('ui-state-default').css('border','none');
                }
                trt.append($('<td class="label" colspan="'+colspan+'">'+serie.label+'</td>'));
                tr.append(tdinp(i,'checkbox','line','line', 'td', serie.lines.show, serie.lines.lineWidth || 3));
                tr.append(tdinp(i,'checkbox','points','points', 'td', serie.points.show, serie.points.radius || 3));
                tr.append(tdinp(i,'checkbox','bars','bars', 'td', serie.bars.show, serie.bars.barWidth || 3));
                $('<td></td>').append(shadow).appendTo(tr);
                tr.append(tdinp(i,'checkbox','fill','fill', 'td', serie.lines.fill));
                
                // Axis radio button
                $('<div></div>').appendTo($('<td></td>').appendTo(tr))
                				.append(makeinp(i+'1','radio','axis'+i,'y-ax1',serie.yaxis ? serie.yaxis===1 : i===0,'1'))
                				.append(makeinp(i+'2','radio','axis'+i,'y-ax2',serie.yaxis ? serie.yaxis===2 : i>0,'2'))
                				.buttonset();
            });
            return canvas;
        }
    });
    

    $.ecoplot.plugin('tooltip',{
        isdefault: true,
        defaults: {
            tooltip_class: 'econometric-plot-tooltip ui-state-default',
            fadein: 50,
            timeout: 500,
            offset: 10
        },
        init: function () {
            this.container().bind("plothover", function (event, pos, item) {
                var instance = $.ecoplot.instance(this),
                    previous = instance.data.tooltip.previous,
                    flot = instance.get_canvas().flot;
                
                if(pos.x || pos.y) {
                    instance.displayposition(pos.x.toFixed(2),pos.y.toFixed(2));
                }
                
                if(flot.getSelection && flot.getSelection()) {
                    return;
                }
                
                if(item) {
                    if(!previous || 
                       (previous.dataIndex !== item.dataIndex ||
                        previous.seriesIndex !== item.seriesIndex)) {
                        var text = instance.tooltipText(item);
                        instance.showTooltip(item.pageX, item.pageY, text);
                        instance.data.tooltip.previous = item;
                    }
                }
                else if(instance.data.tooltip.container) {
                    instance.timeoutTooltip();
                }
            });

        },
        displayposition: function (x,y) {
            if(this.data.tooltip.display) {
            }
        },
        tooltipText: function (item) {
            var options = this.settings(),
                x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2),
                series = item.series,
                d = series.data[item.dataIndex],
                text = series.label,
                canvas = this.get_canvas();
            function todate(v) {
                if(typeof v == 'string') {
                    v = parseFloat(v);
                }
                v = new Date(v);
                return $.datepicker.formatDate(options.dates.format, v); 
            }
            if(d.length === 3) {
                var v = d[2],
                    typ = v.type || series.extratype;
                text = $.isnothing(v.value) ? v : v.value;
                if(typ === 'date') {
                    text = todate(text);
                }
            }
            if(canvas.type === 'timeseries') {
                x = todate(x);
            }
            text += " (" + x + "," + y + ")";
            return text;
        },
        clearTooltip: function () {
            var tooltip = this.data.tooltip;
            if(tooltip.container) {
                tooltip.container.remove();
            }
            tooltip.container = null;
            tooltip.over = null;
            tooltip.previous = null;
            tooltip.timeout = null;
        },
        // Set a timeout to the tooltip
        timeoutTooltip: function () {
            var instance = this,
                options = this.settings().tooltip,
                tooltip = instance.data.tooltip;
            if(!tooltip.over) {
                tooltip.timeout = setTimeout(function (){
                    instance.clearTooltip();
                }, options.timeout );
            }
        },
        showTooltip: function (x, y, contents) {
            var instance = this,
                tooltip = instance.data.tooltip,
                options = this.settings(),
                elem = this.get_canvas().elem,
                width = elem.width(),
                height = elem.height(),
                position = elem.offset(),
                xr = parseInt(x - position.left),
                yr = parseInt(y - position.top),
                offset = options.tooltip.offset,
                tltp,w,h;
            this.clearTooltip();
            this.data.tooltip.container = tltp = $('<div></div>').css({display: 'none'
            }).addClass(options.tooltip.tooltip_class)
              .html(contents)
              .mouseenter(function () {
                  var timeout = tooltip.timeout;
                  if(timeout) {
                      clearTimeout(timeout);
                      tooltip.timeout = null;
                  }
                  tooltip.over = true;
            }).mouseleave(function (){
                tooltip.over = false;
                instance.timeoutTooltip();
            }).appendTo(elem);
            w = tltp.width();
            h = tltp.height();
            if(xr+w > 0.9*width) {
                xr = Math.max(xr - w - offset,0);
            }
            else {
                xr = xr + offset;
            }
            if(yr+h > 0.9*height) {
                yr = Math.max(yr - h - offset,0);
            }
            else {
                yr = yr + offset;
            }
            tltp.css({
                position: 'absolute',
                top:yr,
                left:xr});
            tltp.fadeIn(options.tooltip.fadein);
        }
    });


    $.ecoplot.plugin('command',{
        isdefault: true,
    	defaults : {
    		show: true,
    		entry: null,
    		classname: 'command',
    		container: null,
    		symbol: null,
    	},
        layout: function () {
        	var command = this.settings().command,
        		container = $(container);
        	if(!container.length) {
        		container = this.data.menu.upper;
        	}
        	if(!container.length) {
        		$.ecoplot.error('Could not find a suitable container for the command plugin');
        	}
        	else {
        		var inp = $('input[type="text"]',container);
        		if(!inp.length) {
        			inp = $('<input type="text">').appendTo(container);
        		}
        		inp.attr('name',"commandline");
        		if(command.symbol)  {
        			inp.val(command.symbol+"");
        		}
        		if(command.show) {
        			container.show();
        		}
        		this.data.command.input = inp;
        	}
        },
        get_input_data: function() {
        	var input = this.data.command.input;
        	if(input) {
        		return {'command':input.val()}
        	}
        }
    });
    

    /*
     * Add start and end date inputs. These are useful when loading
     * timeseries data
     */
    $.ecoplot.plugin('dates',{
        isdefault: true,
    	defaults: {
            show: true,
            label: 'Period',
            middle: '-',
            format: "d M yy",
            cn: "ts-input-date",
            default_month_interval: 12,
            start: null,
            end: null,
            classname: 'dateholder menu-item',
        },
        layout: function() {
        	var options = this.settings().dates,
        		dates = this.data.dates,
                el = $('<div></div>').addClass(options.classname).appendTo(this.data.menu.lower);
        	dates.container = el;
            dates.start = $('<input type="text" name="start">').addClass(options.cn).val(options.start),
            dates.end = $('<input type="text" name="end">').addClass(options.cn).val(options.end);
            if(options.label) {
                el.append($('<label>'+options.label+'</label>'));
            }
            el.append(dates.start);
            if(options.middle) {
            	el.append($('<label class="middle">'+options.middle+'</label>'));
            }
            el.append(dates.end);
            if(!options.show) {
                el.hide();
            }
            this.decorate_dates();
        },
        decorate_dates: function() {
        	var options = this.settings().dates,
        		self = this;
            $('.'+options.cn,this.container()).datepicker({
                defaultDate: +0,
                showStatus: true,
                beforeShowDay: $.datepicker.noWeekends,
                dateFormat: options.format, 
                firstDay: 1, 
                changeFirstDay: false
            });
            $('input', this.data.dates.container).change(function() {
            	self.container().trigger('load');
            });
        },
        _canvas_selection: function(e, canvas) {
	        if(canvas.need_redraw === null || canvas.need_redraw === undefined) {
	        	return;
	        }
        	var start = canvas.need_redraw.start.getTime(),
        		end = canvas.need_redraw.end.getTime();
        	canvas.need_redraw = null;
        	if(canvas.type === 'timeseries') {
        		var axis = canvas.flot.getAxes()
        		canvas.flot.setSelection({xaxis: {from: start, to: end},
        								  yaxis: {from: axis.yaxis.min, to: axis.yaxis.max}});
        	}
        },
        init : function() {
        	var dates = this.settings().dates,
            	td, v1, v2;
            if(dates.end) {
                td = new Date(dates.end);
            }
            else {
                td = new Date();
            }
            v2 = $.datepicker.formatDate(dates.format, td);
            if(!dates.start) {
                td.setMonth(td.getMonth() - dates.default_month_interval);
            }
            else {
                td = new Date(dates.start);
            }
            v1 = $.datepicker.formatDate(dates.format, td);
            dates.start = v1;
            dates.end = v2;
            this.container().bind('get_canvas', this._canvas_selection)
        },
        get_input_data: function() {
        	var dates = this.data.dates;
        	return {'start':dates.start.val(),
        			'end':dates.end.val()};
        }
    });

    /**
	 * Add Toolbar items as specified in the options.toolbar array.
	 */
    $.ecoplot.plugin('toolbar',{
        isdefault: true,
    	defaults: {
    		render_as: 'buttons',
    		classname: 'toolbar',
    		display: ['zoomout','reload','legend','edit','saveimage','about']
    	},
    	layout: function () {
            var plugins = this.settings().plugins,
                options = this.settings().toolbar,
            	container = $('<div></div>').addClass(options.classname);
            
            if(options.render_as == 'buttons') {
            	var inner = $('<span></span>').appendTo(container);
            	this.data.toolbar.container = inner;
            	container.addClass('menu-item');
            	container.appendTo(this.data.menu.lower);
            	container.show();
            }
            else {
            	this.data.toolbar.container = container.hide();
            }
            
            this.container().bind('ecoplot-ready', function(e,instance) {
            	var options = instance.settings().toolbar,
            		toolbar = instance.data.toolbar,
            		container = toolbar.container,
            		cid = instance.container().attr('id');
            	
            	$.each(options.display, function (i,name) {
	                var menu = $.ecoplot.tool(name);
	                if(menu && plugins.indexOf(menu.plugin) !== -1) {
	                    var tel,eel,ico;
	                    	id = cid+'_'+menu.classname;
	                    if(!menu.type || menu.type === 'button') {
	                    	tel = $('<button>'+menu.title+'</button>').attr('title',menu.title);
	                    }
	                    else if(menu.type === 'checkbox') {
	                        tel = $('<input type="checkbox"/>');
	                        eel = $('<label>'+menu.title+'</label>').attr('for',id);
	                    }
	                    if(tel) {
	                    	tel.addClass(menu.classname).attr('id',id).appendTo(container);
	                        if(eel) {
	                            container.append(eel);
	                        }
	                        ico = {};
	                        if(menu.icon) {
	                            ico.primary = menu.icon;  
	                        }
	                        tel.button({
	                            text: menu.text || false,
	                            icons: ico
	                        });
	                        if(menu.decorate) {
	                            menu.decorate(tel,instance);
	                        }
	                    }
	                }
	                else {
	                    $.ecoplot.info('Menu '+name+' not available.');
	                }
	            });
            	
            });
        }
    });
    
    
    $.ecoplot.plugin('resizable', {
        isdefault: true,
    	defaults: {
    		disabled: true
    	},
    	init: function () {
    		var options = this.settings().resizable;
    		if(!options.disabled) {
    			this.container().resizable(options);
    		}
    	}
    });
    
    
    $.ecoplot.plugin('about', {
        tools: {
            about: {
                classname: 'about',
                title: 'About Economeric Plotting Plugin',
                icon: "ui-icon-contact",
                decorate: function (b,el) {
                    b.click(function (e) {
                        var info = $.ecoplot.info(),
                            html = "<div class='econometric-about-panel definition-list'>" +
                                   "<dl><dt>Version</dt><dd>"+info.version+"</dd></dl>"+
                                   "<dl><dt>Author</dt><dd>" + info.authors + "</dd></dl>" +
                                   "<dl><dt>Web page</dt><dd><a href='" + info.home_page +
                                   "' target='_blank'>" + info.home_page + "</a></dd></dl>" +
                                   "<dl><dt>jQuery</dt><dd>" + $.fn.jquery + "</dd></dl>" +
                                   "<dl><dt>Flot</dt><dd>" + $.plot.version + "</dd></dl>" +
                                   "</div>";
                        $('<div title="Econometric plugin"></div>').html(html)
                             .dialog({modal: true,
                                     draggable: false,
                                     resizable: false,
                                     width: 500});
                    });
                }
            }
        }
    });
    
    
    /*
     * Add predifiend time-windows to the menubar
     */
    $.ecoplot.plugin('windows', {
    	isdefault: true,
    	defaults: {
    		windows: null,
    		className: 'windows',
    	},
    	layout: function() {
    		var self = this,
    			settings = this.settings(),
    			options = settings.windows,
    			inner;
    		if(options.windows === null) {
    			return;
    		}
    		inner = $('<div class="windows menu-item"></div>');
    		$.each(options.windows, function(i, window) {
    			$.ecoplot.button(window).appendTo(inner).data('window',window);
    		});
    		if(inner.children().length > 0) {
    			inner.appendTo(this.data.menu.lower).show();
                inner.children().click(function() {
                	var dates = self.data.dates,
                		window = $(this).data('window'),
                		months, start, end;
                	if(dates && window) {
                		end = new Date(dates.end.val());
                		start = new Date(dates.end.val());
                		months = parseInt(window.substring(0,window.length-1));
                		if(window.substring(window.length-1).toLowerCase() === 'y') {
                			months *= 12;
                		}
                		start.setMonth(start.getMonth() - months);
                		dates.start.val($.datepicker.formatDate(settings.dates.format, start)).trigger('change');
                	}
                });
    		}
    	}
    });
    
    // /////////////////////////////////////////////////
    // Excel like functionality.
    // /////////////////////////////////////////////////
    //$.ecoplot.shiftf9 = function () {
    //    $(document).bind('keydown','Shift+f9', function (event) {
    //        $('.'+$.ecoplot.plugin_class).each(function () {
    //            var $this = $(this); 
    //            $this.trigger("load");
    //            this.options.elems.commandline.bind('keydown','Shift+f9', function (event) {
    //                $this.trigger("load");
    //           });
    //            this.options.dates.start.bind('keydown','Shift+f9', function (event) {
    //                $this.trigger("load");
    //            });
    //            this.options.dates.end.bind('keydown','Shift+f9', function (event) {
    //                $this.trigger("load");
    //            });
    //        });
    //    });
    //};

}(jQuery));
