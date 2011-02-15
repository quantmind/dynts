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

(function(jQuery){

    /* Add hotkeys plugin if not already available
     *
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
                }
        };

        function keyHandler( handleObj ) {
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

        jQuery.each([ "keydown", "keyup", "keypress" ], function() {
            jQuery.event.special[ this ] = { add: keyHandler };
        });
    }
})(jQuery);

/* 
 * Econometric Ploting Plugin for jQuery
 * 
 * version: 0.4
 * 
 * @requires jQuery v1.4 or Later
 * @requires jQuery-UI v1.8 or Later
 * @requires Flot v0.6 or Later
 *
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
            var _version = "0.4";
            var _plugin_class = "econometric-plot";
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
                    css:null,
                    show:true,
                    symbol:null
            };

            var showPanel = function(p,el) {
                $('.secondary .panel').hide();
                if(p) {
                    el.options.elems.body.addClass('with-panel');
                    p.show();
                }
                if(el.options.canvases) {
                    el.options.canvases.render();
                }
            };
            var hidePanel = function(name,el) {
                $('.secondary .panel').hide();
                el.options.elems.body.removeClass('with-panel');
                if(el.options.canvases) {
                    el.options.canvases.render();
                }
            };

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
                                               $this.trigger('load',[$this, this]);
                                           });
                                       }
                                   },
                                   {
                                       classname: 'options',
                                       title: "Edit plotting options",
                                       icon: "ui-icon-image",
                                       type: "checkbox",
                                       decorate: function(b,el) {
                                           b.toggle(
                                                   function() {
                                                       if(el.options.canvases) {
                                                           showPanel(el.options.canvases.current.panel,el);
                                                       }
                                                   },
                                                   function() {
                                                       if(el.options.canvases) {
                                                           hidePanel(el.options.canvases.current.panel,el);
                                                       }
                                                   }
                                           );
                                       }
                                   }
                                   ];

            this.siteoptions = siteoptions;

            this.defaults = {
                    responsetype:   'json',
                    requestMethod:  'get',
                    elems: {},
                    dates: {
                        show: true,
                        label: 'Period',
                        format: "d M yy",
                        cn: "ts-input-date"
                    },
                    command: {show: true, entry: null},
                    toolbar: default_toolbar,
                    commandline: default_command_line,
                    showplot: function(i) {return true;},
                    requestParams: {},
                    show_tooltip: true,
                    autoload: true,
                    load_url: null,
                    loaderimage: 'ajax-loader.gif',
                    flot_options: {
                        xaxis: {}
                    },
                    paginate: null,
                    infoPanel: 'ecoplot-info',
                    min_height: 200,
                    defaultFade: 300,
                    default_month_interval: 12,
                    classname: 'ts-plot-module',
                    errorClass: 'dataErrorMessage',
                    canvasClass: 'ts-plot-module-canvas',
                    convasContClass: 'ts-plot-module-canvas-container',
                    startLoading: function($this) {
                        var co = this.elems;
                        co.loader.css({'display':'block'});
                        co.canvas_cont.css({'opacity':'0.4'});
                    },
                    stopLoading: function($this) {
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
                    if (typeof console !== "undefined" && typeof console.debug !== "undefined") {
                        console.log('$.ecoplot: '+ s);
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
             * Set default dates in the date panel.
             */
            function _set_default_dates($this)  {
                var options = $this[0].options,
                    dates = options.dates,
                    td, v1, v2;
                if(options.end) {
                    td = new Date(options.end);
                }
                else {
                    td = new Date();
                }
                v2 = $.datepicker.formatDate(dates.format, td);
                if(!options.start) {
                    td.setMonth(td.getMonth() - options.default_month_interval);
                }
                else {
                    td = new Date(options.start);
                }
                v1 = $.datepicker.formatDate(dates.format, td);
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
                var opt = $this[0].options;
                var elems = opt.elems;

                $(window).resize(function() {
                    if(opt.canvases) {
                        opt.canvases.render();
                    }
                });

                $.each(events, function(id,eve) {
                    log('Registering event '+id);
                    eve.register($this);
                });
            }

            function _get_data($this)  {
                var opt = $this[0].options;
                var ticker = opt.elems.commandline.val();
                if(!ticker) {return null;}
                return {
                    start: opt.dates.start.val(),
                    end: opt.dates.end.val(),
                    period:'',
                    command:ticker
                };
            }

            /**
             * Create the editing panel for a given Flot canvas
             */
            function _editpanel(data, showplot, oldcanvas) {
                // check if oldcanvas is the same. If so keep it!
                var newcanvas = data;
                var table = null;
                var body  = null;
                var oldbody = null;
                var oseries = [];
                if(!oldcanvas) {
                    log('Creating editing panel.');
                    table = $('<table class="plot-options"></table>');
                    var head = $('<tr></tr>').appendTo($('<thead></thead>').appendTo(table));
                    head.html('<th>serie</th><th>line</th><th>points</th><th>bars</th><th>y-axis1</th><th>y-axis2</th>');
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
                var tdinp = function(type,name,value,checked) {
                    var check = $('<input type="'+type+'" name="'+name+'" value="'+value+'">');
                    if(checked) {
                        check.attr('checked',true);
                    }
                    return $('<td class="center"></td>').append(check);
                };
                var checkmedia = function(med,show) {
                    if(med) {
                        if(med.show === undefined) {
                            med.show = show;
                        }
                    }
                    else {
                        med = {show: show};
                    }
                    return med;
                };
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
                    tr.append($('<td></td>'));
                    trt.append($('<td class="label" colspan="6">'+serie.label+'</td>'));
                    tr.append(tdinp('checkbox','line','line', serie.lines.show));
                    tr.append(tdinp('checkbox','points','points', serie.points.show));
                    tr.append(tdinp('checkbox','bars','bars', serie.bars.show));
                    tr.append(tdinp('radio','axis'+i,'y-ax1',serie.yaxis ? serie.yaxis===1 : i===0));
                    tr.append(tdinp('radio','axis'+i,'y-ax2',serie.yaxis ? serie.yaxis===2 : i>0));
                    circle += 1;
                });
                return table;
            }

            /**
             * Internal function for adding a new Flot canvas
             */
            function _add(options, el_, data_, oldcanvas, panel) {
                el_.addClass(options.canvasClass);
                var typ = data_.type;
                log('Adding '+ typ + ' data to flot canvases.');
                if(typ === "timeseries") {
                    typ = "time";
                }
                else {
                    typ = null;
                }

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
                        var serie = series[i];
                        serie.lines.show  = $("input[name='line']",el).attr('checked');
                        serie.points.show = $("input[name='points']",el).attr('checked');
                        serie.bars.show = $("input[name='bars']",el).attr('checked');
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
                    this.flot = $.plot(this.elem, adata, zoptions);
                    return this;
                };

                var showplot = options.showplot;
                if(oldcanvas && oldcanvas.options.xaxis.mode === typ) {
                    oldcanvas.name = data_.name;
                    oldcanvas.edit = _editpanel(data_,showplot,oldcanvas);
                    oldcanvas.series = data_.series;
                    data_ = oldcanvas;
                }
                else {
                    data_.panel  = panel;
                    data_.render = renderflot;
                    data_.options = $.extend(true, {}, options.flot_options, data_.options);
                    data_.options.xaxis.mode = typ;
                    data_.edit = _editpanel(data_,showplot);
                    panel.html('').append($('<h2>Series options</h2>')).append(data_.edit);
                }
                data_.elem   = el_;
                return data_;
            }

            /**
             * Internal function for rendering flot
             */
            var _render = function(idx,opts) {
                var all = this.all;
                if(all.length > 0) {
                    var c = this.current;
                    if(idx!==undefined && idx>=0 && idx < all.length) {
                        c = all[idx];
                    }
                    if(c !== this.current) {
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
            };

            /**
             * Internal function for setting up one or more flot plot depending on data.
             * It creates the options.canvases object of the form:
             * 
             * options.canvases = {
             *      all: Array of canvases
             *      height: height of canvas
             *      current: index of current canvas or null
             *      }
             */
            function _set_new_canavases($this,data) {
                var options = $this[0].options;
                var container = options.elems.canvas_cont;
                container.children().fadeOut(options.defaultFade).remove();
                var outer = $('<div></div>').appendTo(container).height(container.height());
                var datac,typ;
                var oldcanvases  = options.canvases; 
                options.canvases = {current: null,
                        render: _render};
                canvases = [];
                options.canvases.all = canvases;

                var optpanel = function(c) {
                    // create options pnel if not available
                    var cn = 'option'+c;
                    var opt = $('.secondary .panel.'+cn,$this);
                    if(!opt.length) {
                        var holder = $('.secondary',$this);
                        opt = $('<div class = "panel '+cn+'"></div>').appendTo(holder);
                    }
                    return opt;
                };
                var oldcanvas = function(c) {
                    if(oldcanvases) {
                        if(oldcanvases.all.length > c) {
                            return oldcanvases.all[c];
                        }
                    }
                };

                if(data) {
                    if(data.length === 1) {
                        canvases.push(_add(options,outer,data[0],oldcanvas(0),optpanel(0)));
                    }
                    /* Setup tabs if data has more than one plot*/
                    else {
                        /* Setup tabs */
                        var cid, cv;
                        var ul = $('<ul></ul>').appendTo(outer);
                        $.each(data, function(i,v) {
                            cid = 'canvas' + i;
                            ul.append($('<li><a href="#' + cid + '">' + v.name + '</a></li>'));
                            cv  = $('<div></div>').attr('id',cid);
                            outer.append(cv);
                            canvases.push(_add(options,cv,v,oldcanvas(i),optpanel(i)));
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
                var options = $this[0].options;
                var elems = options.elems;
                if(elems.info) {
                    elems.info.html("");
                }
                _set_new_canavases($this, data);
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
                    params[key] = typeof param === "function" ? param() : param;
                });
                params = $.extend(true, params, dataplot);
                options.startLoading($this);
                $.ajax({url: options.load_url,
                    type: options.requestMethod,
                    data: $.param(params),
                    dataType: options.responsetype,
                    success: function(data) {
                        log("Got the response from server");
                        var ok = true;
                        if(options.parse)  {
                            try {
                                data = options.parse(data,$this);
                            }
                            catch(e) {
                                ok = false;
                                log("Failed to parse. Error in line " + e.lineNumber + ": " + e);
                            }
                        }
                        options.stopLoading($this);
                        if(ok)  {
                            try {
                                _finaliseLoad($this,data);
                            }
                            catch(e2) {
                                log("Failed to data. Error in line " + e2.lineNumber + ": " + e2);
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
                    var eco = $.ecoplot;
                    var cln = eco.plugin_class;
                    var options = _parseOptions(options_, eco.defaults);
                    var $this = $(this).attr({'id':cln+"_"+i}).addClass(eco);
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
                        $this.trigger("load");
                    }
                    $this.fadeIn(options.defaultFade);
                    if(options.layout) {
                        options.layout($this);
                    }
                });
            }


            /////////////////////////////////////////////////////////////////
            //		API FUNCTIONS AND PROPERTIES
            /////////////////////////////////////////////////////////////////
            this.construct          = _construct;
            this.paginate           = null;
            this.set_default_dates  = _set_default_dates;
            this.loadData           = _request;
            this.addEvent           = function(e){_addelement(e,events);};
            this.removeEvent        = function(id){delete events[id];};
            this.debug              = function(){return debug;};
            this.setdebug           = function(v){debug = v;};
            this.log                = log;
            this.version            = _version;
            this.plugin_class       = _plugin_class;

            this.addMenu = function(menu) {
                menubar[menu.name] = menu;
            };
            this.getmenu = function(name,$this) {
                var menu = menubar[name];
                if(menu) {
                    return menu.create($this[0]);
                }
            };
        }
    });



    $.fn.extend({
        ecoplot: $.ecoplot.construct
    });


///////////////////////////////////////////////////
//  Some Random Functions
///////////////////////////////////////////////////

    /*
     * Excel like functionality.
     */
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



///////////////////////////////////////////////////
//  DEFAULT EVENTS
///////////////////////////////////////////////////
    $.ecoplot.addEvent({
        id: 'load',
        register: function($this) {
            $this.bind("load", function(event, elem) {
                if(!elem) {
                    elem = $(this);
                }
                elem.trigger('pre-reload',[elem, this]);
                $.ecoplot.loadData(elem);
                elem.trigger('after-reload',[elem, this]);
            });
        }
    });

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


    $.ecoplot.addEvent({
        id: 'tooltip',
        register: function($this) {
            var options = $this[0].options;
            var cl = 'econometric-plot-tooltip';
            function showTooltip(x, y, contents) {
                $('<div class="'+cl+'">' + contents + '</div>').css( {
                    position: 'absolute',
                    display: 'none',
                    top: y + 5,
                    left: x + 5
                }).appendTo("body").fadeIn(200);
            }

            $this.bind("plothover", function (event, pos, item) {
                if(!pos.x) {
                    return;
                }
                $("#x").text(pos.x.toFixed(2));
                $("#y").text(pos.y.toFixed(2));

                if(options.show_tooltip) {
                    var canvas = options.canvases.current;
                    if (item) {
                        if(previousPoint || previousPoint !== item.datapoint) {
                            previousPoint = item.datapoint;

                            $("."+cl).remove();
                            var x = item.datapoint[0].toFixed(2),
                            y = item.datapoint[1].toFixed(2);
                            if(canvas.type === 'timeseries') {
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
//  MENUBAR
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
                if(!el.type || el.type === 'button') {
                    tel = $('<button id="'+id+'" class="'+el.classname+'">'+el.title+'</button>');
                }
                else if(el.type === 'checkbox') {
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
//  DEFAULT PAGINATION
//  This can be overritten
///////////////////////////////////////////////////
    $.ecoplot.paginate = function($this) {
        var options = $this[0].options;
        var elems   = options.elems;

        elems.menu = $('<div class="menu"></div>').appendTo($this);
        elems.body = $('<div class="body"></div>').appendTo($this);
        var page  = $('<div class="main"></div>').appendTo(elems.body);
        var page2 = $('<div class="secondary"></div>').appendTo(elems.body);

        elems.canvas_cont  = $('<div class="canvas-container"></div>').appendTo(page);
        elems.options = $('<div class="panel options"></div>').appendTo(page2);
        elems.logger  = $('<div class="panel logger"></div>').appendTo(page2);
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
            elems.commandline.val(cmdlin.symbol+"");
        }
        if(!cmdlin.show) {
            upperm.hide();
        }
        $.ecoplot.set_default_dates($this);
        options.layout = function(el) {
            var options = el[0].options;
            elems = options.elems;
            var height = el.height();
            if(height < 10) {
                height = options.height || options.min_height;
            }
            var h = Math.max(height - elems.menu.height(),30);
            elems.body.height(h);
            elems.canvas_cont.height(h-10).css({'margin':'5px 0'});
            el.height('auto');
        };
    };

})(jQuery);
