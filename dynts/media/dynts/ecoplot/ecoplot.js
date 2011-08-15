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


/*global jQuery */
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
    Usage Note:  
    -----------

    $('.ploting-elems').ecoplot(options);

    options is an object containing several input parameters. All parameters
    have sensible default values apart from one which
    needs to supplied.

      url: String for the remote data provider URL.

    The most common options are:

     * flot_options: Object containing Flot-specific options
     * dates: Object for specifying how dates are displayed
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
            instances = [],
            plugins = {},
            extraTools = {},
            events = {},
            menubar = {},
            debug = false,
            default_logger = {
                log: function (msg,level) {console_logger(msg);},
                info : function (msg) {console_logger(msg);},
                debug : function (msg) {console_logger(msg);},
                error : function (msg) {console_logger(msg);}                
            },
            default_command_line = {
                css:null,
                show:true,
                symbol:null
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
                            },
                   'about': {
                               classname: 'about',
                               title: 'About Economeric Plotting Plugin',
                               icon: "ui-icon-contact",
                               decorate: function (b,el) {
                                   b.click(function (e) {
                                       var html = "<div class='econometric-about-panel definition-list'>" +
                                                  "<dl><dt>Version</dt><dd>"+version+"</dd></dl>"+
                                                  "<dl><dt>Author</dt><dd>" + authors + "</dd></dl>" +
                                                  "<dl><dt>Web page</dt><dd><a href='" + home_page +
                                                  "' target='_blank'>" + home_page + "</a></dd></dl>" +
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
            },
            defaults = {
               elems: {},
               dates: {
                   show: true,
                   label: 'Period',
                   format: "d M yy",
                   cn: "ts-input-date",
                   default_month_interval: 12,
                   start: null,
                   end: null
               },
               command: {show: true, entry: null},
               toolbar: ['zoomout','reload','legend','edit','saveimage','about'],
               commandline: default_command_line,
               showplot: function (i) {return true;},
               show_tooltip: true,
               flot_options: {
                   xaxis: {},
                   legend: {
                       show:true,
                       position: "ne"
                       }
               },
               paginate: null,
               infoPanel: 'ecoplot-info',
               min_height: 200,
               defaultFade: 300,
               classname: 'ts-plot-module',
               errorClass: 'dataErrorMessage'
           };
        
        
        ///////////////////////////////////////////////////////
        //  DEFAULT PAGINATION
        //
        // To override this set ``paginate`` int the options.
        ///////////////////////////////////////////////////////
        function default_paginate(instance) {
            var options = instance.settings(),
                container = instance.container(),
                elems = options.elems,
                cmdlin = options.commandline,
                upperm = $('<div class="menubar upper ui-widget-header"></div>'),
                lowerm = $('<div class="menubar lower ui-widget-header"></div>');

            // Add to containers, the menu and the main body
            elems.menu = $('<div class="menu"></div>').appendTo(container);
            elems.body = $('<div class="body ui-widget-content"></div>')
                            .appendTo(container).height(options.height);
            
            // Add two pages to the body container
            var page  = $('<div class="main"></div>').appendTo(elems.body);
            var page2 = $('<div class="secondary"></div>').appendTo(elems.body);

            instance.canvas_container(true).appendTo(page);
            
            if(instance.edit_container) {
                instance.edit_container(null,true).appendTo(page2);
            }

            /* The menu bar */
            elems.menu.append(upperm).append(lowerm);

            elems.commandline = $.ecoplot.getmenu('command',container).appendTo(upperm);
            $.ecoplot.getmenu('dates',container).appendTo(lowerm);
            lowerm.append($.ecoplot.getmenu('toolbar',container));
            lowerm.append($('<div></div>').addClass(options.jsondata.loader_class));

            if(cmdlin.symbol)  {
                elems.commandline.val(cmdlin.symbol+"");
            }
            if(!cmdlin.show) {
                upperm.hide();
            }
            instance.layout = function () {
                var options = this.settings(),
                    elems = options.elems,
                    container = this.container(),
                    height = container.height(),
                    h;
                if(height < 10) {
                    height = options.height || options.min_height;
                }
                h = Math.max(height - elems.menu.height(),30);
                elems.body.height(h);
                instance.canvas_container().height(h-10).css({'margin':'5px 0'});
                container.height('auto');
            };
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
            var options = {
                    elems: {}
                },
                cl;
            $.extend(true, options, defaults, options_);
            cl = options.commandline;
            if(!cl) {
                cl = default_command_line;
                options.commandline = cl;
            }
            if(cl.symbol) {
                cl.show = false;
            }
            _set_default_dates(options.dates);
            if(!options.paginate) {
                options.paginate = default_paginate;
            }
            return options;
        }

        /**
         * Set default dates in the date panel.
         */
        function _set_default_dates(dates)  {
            var td, v1, v2;
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
        }

        /**
         * Register ecoplot events
         */
        function _registerEvents(instance) {
            var $this = instance.container();
            $.each(events, function (id,eve) {
                $.ecoplot.log.debug('Registering event '+id);
                eve.register($this);
            });
        }
        
        function make_instance(index_, container_, settings_) {
            return {
                data: {},
                settings: function () { return settings_; },
                index: function () { return index_; },
                container: function () { return container_; }
            };
        }
        /**
         * The jQuery plugin constructor
         */
        function _construct(options_) {
            var options = _parseOptions(options_);
            
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
            
            return this.each(function (i) {
                var $this = $(this),
                    instance_id = $this.data("ecoplot-instance-id"),
                    instance;
                if(typeof instance_id !== "undefined" && instances[instance_id]) {
                    instances[instance_id].destroy();
                }
                instance_id = parseInt(instances.push({}),10) - 1;
                $this.data('ecoplot-instance-id',instance_id)
                     .attr({'id':plugin_class+"_"+instance_id})
                     .addClass(plugin_class);
                
                instance = instances[instance_id] = make_instance(
                        instance_id,$this, options);
                
                // Add plugins
                $.each(plugins, function (name,extension) {
                    instance.data[name] = $.extend({},extension.data || {});                    
                    $.each(extension,function (fname,elem) {
                        if(fname == 'init') {
                            elem.apply(instance);
                        }
                        else if(fname !== 'data') {
                            if($.isFunction(elem)) {
                                elem = make_function (fname,elem);
                            }
                            instance[fname] = elem;
                        }
                    });
                });
                
                this.options = options;
                $this.hide().html("");
                options.paginate(instance);
                _registerEvents(instance);
                $this.show();
                if(instance.layout) {
                    instance.layout();
                }
                $this.trigger('ecoplot-ready',instance);
            });
        }


        /////////////////////////////////////////////////////////////////
        //		API FUNCTIONS AND PROPERTIES
        /////////////////////////////////////////////////////////////////          
        return {
            construct: _construct,
            addEvent: function (e){_addelement(e,events);},
            removeEvent: function (id){delete events[id];},
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
                                 .data("ecoplot-instance-id")] || null;
            },
            log: default_logger,
            'version': version,
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
                    tools[name] = val;
                });
                defaults[pname] = pdata.defaults || {};
                plugins[pname] = pdata;
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
    

    //////////////////////////////////////////////////////////////////////////////
    //  Canvases plugin
    //  This is the main plugin which adds the standard plotting functionalities
    //////////////////////////////////////////////////////////////////////////////
    $.ecoplot.plugin('canvases',{
        defaults : {
            legend_class: 'ecolegend ui-state-default',
            legend_padding: 5,
            legend_draggable: true,
            container_class: 'canvas-container',
            canvas_class: 'ts-plot-module-canvas'
        },
        data: {
            all: [],
            current: null
        },
        init: function() {
            var instance = this;
            this.data.canvases.legend_selector = $.selector_from_class(this.settings().canvases.legend_class);
            this.container().bind('ecoplot-pre-resize',function() {
                var canvas = instance.get_canvas();
                $.ecoplot.log.debug('resizing canvas');
                instance._set_legend_position(canvas);
            });
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
                var c = canvases.all[idx];
                if(c) {
                    c.index = idx;
                    return c;
                }
            }
        },
        canvas_container: function (create) {
            var c = $('.'+this.settings().canvases.container_class,this.container());
            if(!c.length && create) {
                return $('<div></div>').addClass(this.settings().canvases.container_class);
            }
            return c;
        },
        _get_serie_data: function (idx,canvas) {
            return canvas.series;
        },
        // Render a canvas. If idx is null or undefined it renders the current canvas
        canvas_render: function (idx,opts) {
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
            data.elem   = cv;
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
                lw,tw,p,m,leg;
            if(!legend) {return;}
            $('td.legendColorBox',legend).css({'padding-right':'5px'});
            canvas.options.legend.relative_position = null;
            legend.appendTo(c);
            if(rpos) {
                if(rpos.left && rpos.top) {
                    var w = c.width(), h = c.height();
                    lw = Math.min(w - legend.width() - 2*options.legend_padding - 2,parseInt(rpos.left*w));
                    tw = Math.min(h - legend.height() - 2*options.legend_padding - 2,parseInt(rpos.top*h));
                    legend.css({left:lw,top:tw});
                }
            }
            else {
                p = opts.legend.position;
                m = opts.legend.margin;
                if (m[0] === null) {
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
    

    ///////////////////////////////////////////////////
    //  plugin for loading data via ajax
    ///////////////////////////////////////////////////
    $.ecoplot.plugin('jsondata',{
        defaults: {
            autoload:true,
            responsetype: 'json',
            requestMethod: 'get',
            url: '.',
            requestparams: {},
            load_opacity: '0.7',
            loader_class: 'loader',
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
                        decorate: function (b,instance) {
                            b.click(function (e,o) {
                                var inst = $.ecoplot.instance(this);
                                if(inst) {
                                    inst.ajaxload();
                                }
                            });
                        }
                    }
        },
        init: function () {
            var options = this.settings().jsondata;
            if(options.autoload) {
                this.container().bind('ecoplot-ready',function (e,instance) {
                    instance.ajaxload();
                });
            }
        },
        ajaxdata: function () {
            var options = this.settings(),
                elems = options.elems,
                ticker = elems.commandline.val();
            if(!ticker) {return;}
            return {
                start: elems.dates.start.val(),
                end: elems.dates.end.val(),
                period:'',
                command:ticker
            };
        },
        ajaxload: function () {
            var options  = this.settings().jsondata,
                log = $.ecoplot.log,
                instance = this,
                dataplot;
            if(!options.url)  {return;}
            dataplot = this.ajaxdata();
            if(!dataplot) {return;}
            log.info("Sending ajax request to " + options.url);
            log.debug(dataplot.command + ' from ' + dataplot.start + ' end '+ dataplot.end);
            var params   = {
                timestamp: +new Date()
            };
            $.each(options.requestparams, function (key, param) {
                params[key] = typeof param === "function" ? param() : param;
            });
            params = $.extend(true, params, dataplot);
            options.startLoading(this);
            $.ajax({
                url: options.url,
                type: options.requestMethod,
                data: $.param(params),
                dataType: options.responsetype,
                success: function (data) {
                    log.info("Got the response from server");
                    var ok = true;
                    try {
                        data = options.parse(data,instance);
                    }
                    catch(e) {
                        ok = false;
                        log.error("Failed to parse. Error in line ",e);
                    }
                    options.stopLoading(instance);
                    if(ok)  {
                        try {
                            instance._ajaxdone(data);
                        }
                        catch(e2) {
                            log.error("Failed after data has loaded",e2);
                        }
                    }
                }
            });
        },
        _ajaxdone: function (data) {
            var options = this.settings(),
                elems = options.elems;
            if(elems.info) {
                elems.info.html("");
            }
            this.replace_all_canvases(data);
        }
    });
    
    
    $.ecoplot.plugin('zoom',{
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
            this.canvas_render(null,opts);
        }
    });
    
    
    $.ecoplot.plugin('png',{
        tools: {
            'saveimage': {
                           classname: 'save-image',
                           title: "Save as image",
                           icon: "ui-icon-image",
                           decorate: function (b,el) {
                               b.click(function () {
                                   var plot = $.ecoplot.instance(this);
                                   plot.saveAsPng();
                               });
                           }
                          }
        },
        saveAsPng: function () {
            var c = this.get_canvas(),
                elem = c ? c.flot : null;
            if(elem) {
                Canvas2Image.saveAsPNG(elem.getCanvas());
            }
        }
    });
    
    
    ///////////////////////////////////////////////////
    //  Edit plugin
    ///////////////////////////////////////////////////
    $.ecoplot.plugin('edit',{
        defaults: {
            editing_class: 'with-panel',
            container_class: 'panel-options',
            panel_class: 'panel'
        },
        tools: {
            edit: {
                classname: 'options',
                title: "Edit plotting options",
                icon: "ui-icon-copy",
                type: "checkbox",
                decorate: function (b,instance) {
                    b.toggle(
                            function () {
                                instance.showPanel();
                            },
                            function () {
                                instance.hidePanel();
                            }
                    );
                }
            }
        },
        init: function () {
            var options = this.settings().edit,
                instance = this;
            this.data.edit.panel_selector = '.'+options.container_class+' .'+options.panel_class;
            this.container().bind('ecoplot-after-add_canvas', function (event, canvas, oldcanvas) {
                var instance = $.ecoplot.instance(this);
                instance.create_edit_panel(canvas,oldcanvas);
            }).bind('ecoplot-after-canvas_render', function (e) {
                if(instance.edit_active()) {
                    instance.showPanel();
                }
            });
        },
        edit_active: function () {
            var options = this.settings();
            return options.elems.body.hasClass(options.edit.editing_class);
        },
        showPanel: function (idx) {
            var canvas = this.get_canvas(idx),
                options = this.settings();
            this._edit_panels().hide();
            if(canvas) {
                options.elems.body.addClass(options.edit.editing_class);
                this.edit_container(canvas.index).show();
            }
            $.ecoplot.resize();
        },
        hidePanel: function () {
            this._edit_panels().hide();
            this.settings().elems.body.removeClass('with-panel');
            $.ecoplot.resize();
        },
        _edit_panels: function () {
            return $(this.data.edit.panel_selector,this.container());
        },
        edit_container: function (idx,create) {
            var options = this.settings().edit,
                holder = $('.'+options.container_class,this.container());
            if(!holder.length && create) {
                holder = $('<div></div>').addClass(options.container_class);
            }
            if(!$.isnothing(idx) && holder.length) {
                var cn = 'option'+idx,
                    p = $('.panel.'+cn,holder);
                if(!p.length && create) {
                    p = $('<div class = "panel '+cn+'"></div>').appendTo(holder);
                }
                return p;
            }
            else {
                return holder;
            }
        },
        _get_serie_data: function (idx,canvas) {
            var adata = [];
            function show_elem(typ,el) {
                if($("input[name='"+typ+"']",el).attr('checked') ? true : false) {
                    var w = $("input[name='"+typ+"_width']",el).val();
                    return w ? parseInt(w) || 1 : 0;
                }
            }
            this.edit_container(idx).find('tr.serie-option').each(function (i) {
                var el = $(this);
                var serie = canvas.series[i];
                serie.shadowSize = parseInt($("input[name='shadow']",el).val());
                serie.lines.lineWidth  = show_elem('line',el);
                serie.lines.show = serie.lines.lineWidth ? true : false;
                serie.points.radius = show_elem('points',el);
                serie.points.show = serie.points.radius ? true : false;
                serie.bars.barWidth = show_elem('bars',el);
                serie.bars.show = serie.bars.barWidth ? true : false;
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
        create_edit_panel: function (canvas) {
            // check if oldcanvas is the same. If so keep it!
            var idx = this.data.canvases.all.length-1,
                options = this.settings(),
                cn = 'option'+idx,
                body  = null,
                oldbody = null,
                oseries = [],
                showplot = options.showplot,
                edit_panel = this.edit_container(idx,true),
                table;
            
            if(!edit_panel.length) {
                return;
            }
            
            if(!canvas.oseries) {
                var top = $('<div></div>').css({'overflow':'hidden','margin-bottom':'10px'}),
                    h2 = $('<h2>Series</h2>').css({'float':'left','margin':0}).appendTo(top),
                    redraw = $("<button>Redraw</button>").button().click(function() {
                        var instance = $.ecoplot.instance(this);
                        instance._set_legend_position(instance.get_canvas());
                        instance.canvas_render();
                    }).appendTo(top).css({'margin-left':'10px'}); 
                $.ecoplot.log.debug('Creating editing panel.');
                edit_panel.children().remove();
                edit_panel.append(top);
                table = $('<table class="plot-options"></table>').appendTo(edit_panel);
                var head = $('<tr></tr>').appendTo($('<thead class="ui-widget-header"></thead>').appendTo(table));
                head.html('<th>line</th><th>points</th><th>bars</th><th>shadow</th><th>y-axis1</th><th>y-axis2</th>');
                body = $('<tbody class="ui-widget-content"></tbody>').appendTo(table);
            }
            else {
                table = $('table',edit_panel);
                body = $('tbody',table).html('');
                oseries = canvas.oseries;
            }
            //Add a column element to a series row
            function tdinp(type,name,value,checked,w) {
                var check = $('<input type="'+type+'" name="'+name+'" value="'+value+'">'),
                    r;
                if(checked) {
                    check.prop({'checked':true}); // jQuery 1.6.1
                    //check.attr('checked',true);
                }
                r = $('<td class="center"></td>').append(check);
                if(w) {
                    var inp = $('<input type="input" name="'+name+'_width" value="'+w+'">')
                                .width('2em')
                                .css({'margin-left':'3px'});
                    r.append(inp);
                }
                return r;
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
                    shadow;
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
                shadow = $('<input type="input" name="shadow" value="'+ shadow +'">').width('2em');
                var trt = $('<tr class="serie'+i+' serie-title"></tr>').appendTo(body);
                var tr  = $('<tr class="serie'+i+' serie-option"></tr>').appendTo(body);
                if(parseInt((i+1)/2)*2 === i+1) {
                    trt.addClass('ui-state-default');
                    tr.addClass('ui-state-default');
                }
                trt.append($('<td class="label" colspan="6">'+serie.label+'</td>'));
                tr.append(tdinp('checkbox','line','line', serie.lines.show, serie.lines.lineWidth || 3));
                tr.append(tdinp('checkbox','points','points', serie.points.show, serie.points.radius || 3));
                tr.append(tdinp('checkbox','bars','bars', serie.bars.show, serie.bars.barWidth || 3));
                $('<td></td>').append(shadow).appendTo(tr);
                tr.append(tdinp('radio','axis'+i,'y-ax1',serie.yaxis ? serie.yaxis===1 : i===0));
                tr.append(tdinp('radio','axis'+i,'y-ax2',serie.yaxis ? serie.yaxis===2 : i>0));
            });
            return canvas;
        }
    });
    

    $.ecoplot.plugin('tooltip',{
        defaults: {
            tooltip_class: 'econometric-plot-tooltip ui-state-default',
            fadein: 50,
            timeout: 200,
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
                    instance.hideTooltip();
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
            tooltip.previous = null;
        },
        hideTooltip: function () {
            var instance = this,
                options = this.settings().tooltip;
            instance.data.tooltip.timeout = setTimeout(function (){
                instance.clearTooltip();
            }, options.timeout );
        },
        showTooltip: function (x, y, contents) {
            var instance = this,
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
            tltp = $('<div></div>').css({display: 'none'
            }).addClass(options.tooltip.tooltip_class)
              .html(contents)
              .mouseenter(function () {
                var timeout = instance.data.tooltip.timeout;
                if(timeout) {
                    clearTimeout(timeout);
                }
            }).mouseleave(function (){
                instance.hideTooltip();
            }).appendTo(elem);
            this.data.tooltip.container = tltp;
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

///////////////////////////////////////////////////
//  EVENTS & MENUS
///////////////////////////////////////////////////

    $.ecoplot.addEvent({
        id: 'datepicker',
        register: function ($this) {
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

    /**
     * Add Command Input
     */
    $.ecoplot.addMenu({
        name: 'command',
        classname: 'command',
        create: function (elem) {
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
        create: function (elem) {
            var dates = elem.options.dates,
                elems = elem.options.elems,
                el = $('<div class="'+ this.classname + ' menu-item"></div>'),
                start_id = elem.id+'_start',
                end_id = elem.id+'_end',
                start = $('<input id="'+start_id+'" class="'+dates.cn+'" type="text" name="start">'),
                end   = $('<input id="'+end_id+'" class="'+dates.cn+'" type="text" name="end">');
            start.val(dates.start);
            end.val(dates.end);
            if(dates.label) {
                el.append($('<label for_id="'+start_id+'">'+dates.label+'</label>'));
            }
            el.append(start);
            el.append($('<label class="middle">-</label>'));
            el.append(end);
            if(!dates.show) {
                el.hide();
            }
            elems.dates = {'start':start,'end':end};
            return el;
        }
    });


    /**
     * Add Toolbar items as specified in the options.toolbar array.
     */
    $.ecoplot.addMenu({
        name: 'toolbar',
        classname: 'toolbar',
        create: function (elem) {
            var instance = $.ecoplot.instance(elem),
                options = instance.settings(),
                outer = $('<div class="'+ this.classname + ' menu-item"></div>'),
                cid = instance.container().attr('id')+'_'+this.classname,
                container = $('<span id="'+cid+'"></span>').appendTo(outer);
            $.each(options.toolbar, function (i,name) {
                var menu = $.ecoplot.tool(name);
                if(menu) {
                    var tel,eel,ico,
                        id = cid+'_'+menu.classname;
                    if(!menu.type || menu.type === 'button') {
                        tel = $('<button id="'+id+'" class="'+menu.classname+'">'+menu.title+'</button>');
                    }
                    else if(menu.type === 'checkbox') {
                        tel = $('<input id="'+id+'" type="checkbox" class="'+menu.classname+'"/>');
                        eel = $('<label for="'+id+'">'+menu.title+'</label>');
                    }
                    if(tel) {
                        container.append(tel);
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
            return outer;
        }
    });
    
    ///////////////////////////////////////////////////
    //  Excel like functionality.
    ///////////////////////////////////////////////////
    $.ecoplot.shiftf9 = function () {
        $(document).bind('keydown','Shift+f9', function (event) {
            $('.'+$.ecoplot.plugin_class).each(function () {
                var $this = $(this); 
                $this.trigger("load");
                this.options.elems.commandline.bind('keydown','Shift+f9', function (event) {
                    $this.trigger("load");
                });
                this.options.dates.start.bind('keydown','Shift+f9', function (event) {
                    $this.trigger("load");
                });
                this.options.dates.end.bind('keydown','Shift+f9', function (event) {
                    $this.trigger("load");
                });
            });
        });
    };

}(jQuery));
