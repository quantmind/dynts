/* 
 * Econometric Ploting JavaScript Library version @VERSION
 * 
 * @requires jQuery v1.4 or Later
 * @requires jQuery-UI v1.8 or Later
 * @requires Flot v0.6 or Later
 * 
 * Date: @DATE
 *
 */
/*global jQuery */
(function(jQuery){

    /*
     * jQuery Hotkeys Plugin
     * Copyright 2010, John Resig
     * Dual licensed under the MIT or GPL Version 2 licenses.
     *
     * Based upon the plugin by Tzury Bar Yochay:
     * http://github.com/tzuryby/hotkeys
     *
     * Original idea by:
     * Binny V A, http://www.openjs.com/scripts/events/keyboard_shortcuts/
     */
    if(!jQuery.hotkeys) {

        jQuery.hotkeys = {
            
            version: "0.8",

            specialKeys: {
                8: "backspace", 9: "tab", 13: "return", 16: "shift", 17: "ctrl", 18: "alt", 19: "pause",
                20: "capslock", 27: "esc", 32: "space", 33: "pageup", 34: "pagedown", 35: "end", 36: "home",
                37: "left", 38: "up", 39: "right", 40: "down", 45: "insert", 46: "del", 
                96: "0", 97: "1", 98: "2", 99: "3", 100: "4", 101: "5", 102: "6", 103: "7",
                104: "8", 105: "9", 106: "*", 107: "+", 109: "-", 110: ".", 111 : "/", 
                112: "f1", 113: "f2", 114: "f3", 115: "f4", 116: "f5", 117: "f6", 118: "f7", 119: "f8", 
                120: "f9", 121: "f10", 122: "f11", 123: "f12", 144: "numlock", 145: "scroll", 191: "/", 224: "meta"
            },

            shiftNums: {
                "`": "~", "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", 
                "8": "*", "9": "(", "0": ")", "-": "_", "=": "+", ";": ": ", "'": "\"", ",": "<", 
                ".": ">",  "/": "?",  "\\": "|"
            },
            
            keyHandler: function( handleObj ) {
                // Only care when a possible input has been specified
                if ( typeof handleObj.data !== "string" ) {
                    return;
                }
    
                var origHandler = handleObj.handler,
                keys = handleObj.data.toLowerCase().split(" ");
    
                handleObj.handler = function( event ) {
                    // Don't fire in text-accepting inputs that we didn't directly bind to
                    if ( this !== event.target && (/textarea|select/i.test( event.target.nodeName ) ||
                            event.target.type === "text") ) {
                        return;
                    }
    
                    // Keypress represents characters, not special keys
                    var special = event.type !== "keypress" && jQuery.hotkeys.specialKeys[ event.which ],
                    character = String.fromCharCode( event.which ).toLowerCase(),
                    key, modif = "", possible = {}, i;
    
                    // check combinations (alt|ctrl|shift+anything)
                    if ( event.altKey && special !== "alt" ) {
                        modif += "alt+";
                    }
    
                    if ( event.ctrlKey && special !== "ctrl" ) {
                        modif += "ctrl+";
                    }
    
                    // TODO: Need to make sure this works consistently across platforms
                    if ( event.metaKey && !event.ctrlKey && special !== "meta" ) {
                        modif += "meta+";
                    }
    
                    if ( event.shiftKey && special !== "shift" ) {
                        modif += "shift+";
                    }
    
                    if ( special ) {
                        possible[ modif + special ] = true;
    
                    } else {
                        possible[ modif + character ] = true;
                        possible[ modif + jQuery.hotkeys.shiftNums[ character ] ] = true;
    
                        // "$" can be triggered as "Shift+4" or "Shift+$" or just "$"
                        if ( modif === "shift+" ) {
                            possible[ jQuery.hotkeys.shiftNums[ character ] ] = true;
                        }
                    }
    
                    for (i = 0, l = keys.length; i < l; i++ ) {
                        if ( possible[ keys[i] ] ) {
                            return origHandler.apply( this, arguments );
                        }
                    }
                };
            }
        };

        jQuery.each([ "keydown", "keyup", "keypress" ], function() {
            jQuery.event.special[ this ] = { add: jQuery.hotkeys.keyHandler };
        });
    }
}(jQuery));


(function($) {

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

    $.isnothing = function(o) {
        return o === null || o === undefined;
    };
    
    $.ecoplot = (function() {
        
        function console_logger(msg) {
            if (typeof console !== "undefined" && typeof console.debug !== "undefined") {
                console.log(msg);
            }
        }
        
        var _version = "0.4.2",
            _authors = 'Luca Sbardella',
            _home_page = 'https://github.com/quantmind/dynts',
            plugin_class = "econometric-plot",
            instances = [],
            plugins = {},
            extraTools = {},
            events = {},
            menubar = {},
            debug = false,
            default_logger = {
                log: function(msg,level) {console_logger(msg);},
                info : function(msg) {console_logger(msg);},
                debug : function(msg) {console_logger(msg);},
                error : function(msg) {console_logger(msg);}                
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
                               decorate: function(b,instance) {
                                   b.toggle(function() {
                                        $('.legend',instance.container()).hide();
                                    },
                                    function() {
                                        $('.legend',instance.container()).show();
                                    }
                                  );
                               }
                            },
                   'about': {
                               classname: 'about',
                               title: 'About Economeric Plotting Plugin',
                               icon: "ui-icon-contact",
                               decorate: function(b,el) {
                                   b.click(function(e) {
                                       var html = "<div class='econometric-about-panel definition-list'>" +
                                       		      "<dl><dt>Version</dt><dd>" + _version + "</dd></dl>"+
                                                  "<dl><dt>Author</dt><dd>" + _authors + "</dd></dl>" +
                                                  "<dl><dt>Web page</dt><dd><a href='" + _home_page +
                                                  "' target='_blank'>" + _home_page + "</a></dd></dl>" +
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
                   end: null,
               },
               command: {show: true, entry: null},
               toolbar: ['zoomout','reload','legend','edit','saveimage','about'],
               commandline: default_command_line,
               showplot: function(i) {return true;},
               show_tooltip: true,
               flot_options: {
                   xaxis: {}
               },
               paginate: null,
               infoPanel: 'ecoplot-info',
               min_height: 200,
               defaultFade: 300,
               classname: 'ts-plot-module',
               errorClass: 'dataErrorMessage'
           };
           
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
                options.paginate = $.ecoplot.default_paginate;
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
            $.each(events, function(id,eve) {
                $.ecoplot.log.debug('Registering event '+id);
                eve.register($this);
            });
        }
        
        function make_instance(index_, container_, settings_) {
            return {
                data: {},
                logger: function() { return settings_.logger; },
                settings: function() { return settings_; },
                index: function() { return index_; },
                container: function() { return container_; }
            };
        }
        /**
         * The jQuery plugin constructor
         */
        function _construct(options_) {
            var options = _parseOptions(options_);
            
            function make_function(fname,func) {
                if(fname.charAt(0) == '_') {
                    return func;
                }
                else {
                    return function() {
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
            
            return this.each(function(i) {
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
                $.each(plugins, function(name,extension) {
                    instance.data[name] = $.extend({},extension.data || {});                    
                    $.each(extension,function(fname,elem) {
                        if(fname == 'init') {
                            elem.apply(instance);
                        }
                        else if(fname !== 'data') {
                            if($.isFunction(elem)) {
                                elem = make_function(fname,elem);
                            }
                            instance[fname] = elem;
                        }
                    });
                });
                
                this.options = options;
                $this.hide().html("");
                options.paginate($this);
                _registerEvents(instance);
                //$this.fadeIn(options.defaultFade);
                $this.show();
                if(options.layout) {
                    options.layout($this);
                }
                $this.trigger('ecoplot-ready',instance);
            });
        }


        /////////////////////////////////////////////////////////////////
        //		API FUNCTIONS AND PROPERTIES
        /////////////////////////////////////////////////////////////////          
        return {
            construct: _construct,
            addEvent: function(e){_addelement(e,events);},
            removeEvent: function(id){delete events[id];},
            debug: function(){return debug;},
            setdebug: function(v){debug = v;},
            count: function() {return instances.length;},
            instance: function(elem) {
                // get by instance id
                if(instances[elem]) { return instances[elem]; }
                var o = $(elem); 
                if(!o.length && typeof elem === "string") { o = $("#" + elem); }
                if(!o.length) { return null; }
                return instances[o.closest("."+plugin_class)
                                 .data("ecoplot-instance-id")] || null;
            },
            log: default_logger,
            version: _version,
            'plugin_class': plugin_class,
            addMenu: function(menu) {menubar[menu.name] = menu;},
            getmenu: function(name,$this) {
                var menu = menubar[name];
                if(menu) {
                    return menu.create($this[0]);
                }
            },
            tool: function(name) {
                return tools[name];
            },
            plugin: function(pname, pdata) {
                var tbs = pdata.tools || {};
                $.each(tbs, function(name,val) {
                    tools[name] = val;
                });
                defaults[pname] = pdata.defaults || {},
                plugins[pname] = pdata;
            },
            resize: function() {
                $(window).trigger('resize');
            }
        };
    }());



    $.fn.extend({
        ecoplot: $.ecoplot.construct
    });
    
///////////////////////////////////////////////////
//  Default plugins
///////////////////////////////////////////////////

    ///////////////////////////////////////////////////
    //  Canvases plugin
    ///////////////////////////////////////////////////
    $.ecoplot.plugin('canvases',{
        defaults : {
            container_class: 'canvas-container',
            canvas_class: 'ts-plot-module-canvas',
        },
        data: {
            all: [],
            current: null,
        },
        init: function() {
            var instance = this;
            $(window).resize(function() {
                instance.canvas_render();
            });
        },
        get_canvas: function(idx) {
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
        canvas_container: function() {
            return $('.'+this.settings().canvases.container_class,this.container());
        },
        _get_serie_data: function(idx,canvas) {
            return canvas.series;
        },
        // Render a canvas. If idx is null or undefined it renders the current canvas
        canvas_render: function(idx,opts) {
            var canvas = this.get_canvas(idx),
                container = this.canvas_container(),
                height,zoptions,adata;
            if(!canvas) {return;}
            zoptions = canvas.options;
            height = container.height() - $('ul',container).height();
            canvas.elem.height(height);
            if(opts) {
                zoptions = $.extend(true, {}, canvas.options, opts);
                canvas.zoptions = zoptions;
            }
            else if(opts === null) {
                zoptions = canvas.options;
            }
            else if(canvas.zoptions) {
                zoptions = canvas.zoptions;
            }
            adata = this._get_serie_data(canvas.index,canvas);
            canvas.flot = $.plot(canvas.elem, adata, zoptions);
            this.data.canvases.current = canvas.index;
            return canvas;
        },
        // Add a new canvas to the list
        add_canvas: function(data, oldcanvas) {
            var options = this.settings(),
                instance = this,
                $this = this.container(),
                container = this.canvas_container(),
                canvases = this.data.canvases,
                typ = data.type,
                name = data.name,
                idx = canvases.all.length,
                cid = $this.attr('id') + '-canvas' + idx,
                cv = $('<div></div>').attr('id',cid)
                                     .addClass(options.canvases.canvas_class);
            
            if(!idx) {
                $('<ul></ul>').appendTo(container).hide();
            }
            $('ul',container).append($('<li><a href="#' + cid + '">' + name + '</a></li>'));
            cv.appendTo(container);
            $.ecoplot.log.debug('Adding '+ typ + ' ' + name + ' to canvases.');
            if(typ === "timeseries") {
                typ = "time";
            }
            else {
                typ = null;
            }

            if(oldcanvas && oldcanvas.options.xaxis.mode === typ) {
                oldcanvas.name = name;
                oldcanvas.series = data.series;
                data = oldcanvas;
            }
            else {
                data.options = $.extend(true, {}, options.flot_options, data.options);
                data.options.xaxis.mode = typ;
            }
            data.elem   = cv;
            canvases.all.push(data);
            return data;
        },
        // Replace all canvases with new ones
        replace_all_canvases: function(data) {
            var options = this.settings(),
                canvases = this.data.canvases,
                container = this.canvas_container(),
                oldcanvases = canvases.all,
                that = this,
                datac,typ;
            container.children().fadeOut(options.defaultFade).remove();
            canvases.current = null;
            canvases.all = [];
            
            function oldcanvas(c) {
                if(oldcanvases.length > c) {
                    return oldcanvases[c];
                }
            };

            if(data) {
                $.each(data, function(i,v) {
                    that.add_canvas(v,oldcanvas(i));
                });
                if(canvases.all.length == 1) {
                    $('ul',container).remove();
                }
                else {
                    $('ul',container).show();
                    container.tabs({
                        show: function(event,ui) {
                            if(options.canvases.height) {
                                that.canvases.render(ui.index);
                            }
                        }
                    }); 
                }
            }
            this.canvas_render(0);       
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
            parse: function(data,instance){return data;},
            startLoading: function(instance) {
                var options = instance.settings();
                $('.loader',instance.container()).show();
                instance.canvas_container().css({'opacity':options.load_opacity});
            },
            stopLoading: function(instance) {
                $('.loader',instance.container()).css({'display':'none'});
                instance.canvas_container().css({'opacity':'1'});
            }
        },
        tools: {
            'reload': {
                        classname: 'reload',
                        title: "Refresh data",
                        icon: "ui-icon-refresh",
                        decorate: function(b,instance) {
                            b.click(function(e,o) {
                                var inst = $.ecoplot.instance(this);
                                if(inst) {
                                    inst.ajaxload();
                                }
                            });
                        }
                    }
        },
        init: function() {
            var options = this.settings().jsondata;
            if(options.autoload) {
                this.container().bind('ecoplot-ready',function(e,instance) {
                    instance.ajaxload();
                });
            }
        },
        ajaxdata: function() {
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
        ajaxload: function() {
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
            $.each(options.requestparams, function(key, param) {
                params[key] = typeof param === "function" ? param() : param;
            });
            params = $.extend(true, params, dataplot);
            options.startLoading(this);
            $.ajax({
                url: options.url,
                type: options.requestMethod,
                data: $.param(params),
                dataType: options.responsetype,
                success: function(data) {
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
        _ajaxdone: function(data) {
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
                            decorate: function(b) {
                                b.click(function(e) {
                                    var instance = $.ecoplot.instance(this);
                                    if(instance) {
                                        instance.canvas_render(null,null);
                                    }
                                });
                            }
                }
        },
        init: function() {
            this.data.zoom.selecting = false;
            this.container().bind('plotselecting', function() {
                var instance = $.ecoplot.instance(this);
                instance.data.selecting = true;
            }).bind('plotselected', function(event, ranges) {
                var instance = $.ecoplot.instance(this);
                instance.data.selecting = false;
                instance.zoom(ranges);
            });
        },
        zoom: function(ranges) {
            var canvas = this.get_canvas();
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
                           decorate: function(b,el) {
                               b.click(function() {
                                   var plot = $.ecoplot.instance(this);
                                   plot.saveAsPng();
                               });
                           }
                          }
        },
        saveAsPng: function() {
            var c = this.get_canvas();
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
            container_class: 'secondary',
            panel_class: 'panel'
        },
        tools: {
            edit: {
                classname: 'options',
                title: "Edit plotting options",
                icon: "ui-icon-copy",
                type: "checkbox",
                decorate: function(b,instance) {
                    b.toggle(
                            function() {
                                instance.showPanel();
                            },
                            function() {
                                instance.hidePanel();
                            }
                    );
                }
            }
        },
        init: function() {
            var options = this.settings().edit;
            this.data.edit.panel_selector = '.'+options.container_class+' .'+options.panel_class;
            this.container().bind('ecoplot-after-add_canvas', function(event, data, oldcanvas) {
                var instance = $.ecoplot.instance(this);
                instance.create_edit_panel(data,oldcanvas);
            });
        },
        showPanel: function(idx) {
            var canvas = this.get_canvas(idx),
                options = this.settings();
            this._edit_panels().hide();
            if(canvas) {
                options.elems.body.addClass('with-panel');
                canvas.edit.show();
            }
            $.ecoplot.resize();
        },
        hidePanel: function() {
            this._edit_panels().hide();
            this.settings().elems.body.removeClass('with-panel');
            $.ecoplot.resize();
        },
        _edit_panels: function() {
            return $(this.data.edit.panel_selector,this.container());
        },
        edit_container: function(idx,create) {
            var holder = $('.'+this.settings().edit.container_class,this.container());
            if(idx!==null && idx!==undefined && holder.length) {
                var cn = 'option'+idx;
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
        _get_serie_data: function(idx,canvas) {
            var adata = [];
            function show_elem(typ,el) {
                return $("input[name='"+typ+"']",el).attr('checked') ? true : false;
            }
            this.edit_container(idx).find('tr.serie-option').each(function(i) {
                var el = $(this);
                var serie = canvas.series[i];
                serie.lines.show  = show_elem('line',el);
                serie.points.show = show_elem('points',el);
                serie.bars.show = show_elem('bars',el);
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
        create_edit_panel: function(data, oldcanvas) {
            // check if oldcanvas is the same. If so keep it!
            var idx = this.data.canvases.all.length-1,
                options = this.settings(),
                cn = 'option'+idx,
                table = null,
                body  = null,
                oldbody = null,
                oseries = [],
                showplot = options.showplot,
                edit_panel = this.edit_container(idx,true);
            
            if(!edit_panel.length) {
                return;
            }
            
            if(!oldcanvas) {
                $.ecoplot.log.debug('Creating editing panel.');
                edit_panel.children().remove();
                edit_panel.append($('<h2>Series options</h2>'));
                table = $('<table class="plot-options"></table>').appendTo(edit_panel);
                var head = $('<tr></tr>').appendTo($('<thead></thead>').appendTo(table));
                head.html('<th>line</th><th>points</th><th>bars</th><th>y-axis1</th><th>y-axis2</th>');
                body = $('<tbody></tbody>').appendTo(table);
                table.click(function() {
                    data.render();
                });
            }
            else {
                table = oldcanvas.edit;
                body = $('tbody',table).html('');
                oseries = oldcanvas.series;
            }
            //Add a column element to a series row
            function tdinp(type,name,value,checked) {
                var check = $('<input type="'+type+'" name="'+name+'" value="'+value+'">');
                if(checked) {
                    check.prop({'checked':true}); // jQuery 1.6.1
                    //check.attr('checked',true);
                }
                return $('<td class="center"></td>').append(check);
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
            
            var circle = 0;
            $.each(data.series, function(i,serie) {
                var oserie = null;
                if(oseries.length > i) {
                    var os = oseries[i];
                    if(serie.label === os.label) {
                        oserie = os;
                    }
                }
                if(circle>1) {
                    circle = 0;
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
                }
                var trt = $('<tr class="line'+circle+' serie'+i+' serie-title"></tr>').appendTo(body);
                var tr  = $('<tr class="line'+circle+' serie'+i+' serie-option"></tr>').appendTo(body);
                trt.append($('<td class="label" colspan="6">'+serie.label+'</td>'));
                tr.append(tdinp('checkbox','line','line', serie.lines.show));
                tr.append(tdinp('checkbox','points','points', serie.points.show));
                tr.append(tdinp('checkbox','bars','bars', serie.bars.show));
                tr.append(tdinp('radio','axis'+i,'y-ax1',serie.yaxis ? serie.yaxis===1 : i===0));
                tr.append(tdinp('radio','axis'+i,'y-ax2',serie.yaxis ? serie.yaxis===2 : i>0));
                circle += 1;
            });
            data.edit = table;
            return data;
        }
    });
    

    $.ecoplot.plugin('tooltip',{
        defaults: {
            tooltip_class: 'econometric-plot-tooltip',
            fadein: 50,
            timeout: 200,
            offset: 5,
        },
        init: function() {
            this.container().bind("plothover", function(event, pos, item) {
                var instance = $.ecoplot.instance(this),
                    previous = instance.data.tooltip.previous;
                
                if(instance.data.selecting) {
                    return;
                }
                //if(pos.x || pos.y) {
                //    $("#x").text(pos.x.toFixed(2));
                //    $("#y").text(pos.y.toFixed(2));
                //}
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
        tooltipText: function(item) {
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2),
                d = item.series.data[item.dataIndex],
                text = d.length == 3 ? d[2] : item.series.label,
                canvas = this.get_canvas();
            if(canvas.type === 'timeseries') {
                x = new Date(parseFloat(x));
                x = $.datepicker.formatDate(this.settings().dates.format, x);
            }
            text += " (" + x + "," + y + ")";
            return text;
        },
        clearTooltip: function() {
            var tooltip = this.data.tooltip;
            if(tooltip.container) {
                tooltip.container.remove();
            }
            tooltip.container = null;
            tooltip.previous = null;
        },
        hideTooltip: function() {
            var instance = this,
                options = this.settings().tooltip;
            instance.data.tooltip.timeout = setTimeout(function(){
                instance.clearTooltip();
            }, options.timeout );
        },
        showTooltip: function(x, y, contents) {
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
              .mouseenter(function() {
                var timeout = instance.data.tooltip.timeout;
                if(timeout) {
                    clearTimeout(timeout);
                }
            }).mouseleave(function(){
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
        create: function(elem) {
            var instance = $.ecoplot.instance(elem),
                options = instance.settings(),
                outer = $('<div class="'+ this.classname + ' menu-item"></div>'),
                cid = instance.container().attr('id')+'_'+this.classname,
                container = $('<span id="'+cid+'"></span>').appendTo(outer);
            $.each(options.toolbar, function(i,name) {
                var menu = $.ecoplot.tool(name);
                if(menu) {
                    var tel,eel,ico;
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
    //  DEFAULT PAGINATION
    //
    // To override this set ``paginate`` to
    // the options.
    ///////////////////////////////////////////////////
    $.ecoplot.default_paginate = function($this) {
        var options = $this[0].options,
            elems = options.elems,
            cmdlin = options.commandline,
            upperm = $('<div class="menubar upper ui-widget-header"></div>'),
            lowerm = $('<div class="menubar lower ui-widget-header"></div>');

        elems.menu = $('<div class="menu"></div>').appendTo($this);
        elems.body = $('<div class="body ui-widget-content"></div>')
                        .appendTo($this).height(options.height);
        var page  = $('<div class="main"></div>').appendTo(elems.body);
        var page2 = $('<div class="secondary"></div>').appendTo(elems.body);

        elems.canvas_cont  = $('<div class="canvas-container"></div>').appendTo(page);
        elems.options = $('<div class="panel options"></div>').appendTo(page2);
        elems.loader  = $('<div class="loader"></div>');

        /* The menu bar */
        elems.menu.append(upperm).append(lowerm);

        elems.commandline = $.ecoplot.getmenu('command',$this).appendTo(upperm);
        $.ecoplot.getmenu('dates',$this).appendTo(lowerm);
        lowerm.append($.ecoplot.getmenu('toolbar',$this));
        lowerm.append(elems.loader);

        if(cmdlin.symbol)  {
            elems.commandline.val(cmdlin.symbol+"");
        }
        if(!cmdlin.show) {
            upperm.hide();
        }
        options.layout = function(el) {
            var options = el[0].options,
                elems = options.elems,
                height = el.height(),
                h;
            if(height < 10) {
                height = options.height || options.min_height;
            }
            h = Math.max(height - elems.menu.height(),30);
            elems.body.height(h);
            elems.canvas_cont.height(h-10).css({'margin':'5px 0'});
            el.height('auto');
        };
    };
    
    ///////////////////////////////////////////////////
    //  Excel like functionality.
    ///////////////////////////////////////////////////
    $.ecoplot.shiftf9 = function() {
        $(document).bind('keydown','Shift+f9', function(event) {
            $('.'+$.ecoplot.plugin_class).each(function() {
                var $this = $(this); 
                $this.trigger("load");
                this.options.elems.commandline.bind('keydown','Shift+f9', function(event) {
                    $this.trigger("load");
                });
                this.options.dates.start.bind('keydown','Shift+f9', function(event) {
                    $this.trigger("load");
                });
                this.options.dates.end.bind('keydown','Shift+f9', function(event) {
                    $this.trigger("load");
                });
            });
        });
    };

}(jQuery));
