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
    
    $.color_gradient = (function() {
        
        var hexDigits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
        
        // checks, if there is any unvalid digit for a hex number
        function checkHexDigits(s) {
            var j, found;
            for(var i = 0; i < s.length; i++) {
                found   = false;
                for(j = 0; j < hexDigits.length; j++)
                    if(s.substr(i, 1) == hexDigits[j])
                        found   = true;
                if(!found)
                    return false;
            }
            return true;
        }
        
        // checks, if a given number is a hexadezimal number
        function checkHex(hex) {
            if (!hex || hex==""  || hex=="#") throw "No valid hexadecimal given.";
            hex = hex.toUpperCase();            
            switch(hex.length) {
                case 6:
                    hex = "#" + hex;
                    break;
                case 7:
                    break;
                case 3:
                    hex = "#" + hex;
                    break;
                case 4:
                    hex = "#" + hex.substr(1, 1) + hex.substr(1, 1) + hex.substr(2, 1) + hex.substr(2, 1) + hex.substr(3, 1) + hex.substr(3, 1);
                    break;
            }
            if(hex.substr(0, 1) != "#" || !checkHexDigits(hex.substr(1))) {
                throw "No valid hexadecimal given.";
            }
            return hex; 
        }
        
        // generates a rgb value, using a hex value
        function hex2rgb(hex) {        
            var rgb = [];
            try {
                hex = checkHex(hex);
                rgb[0]=parseInt(hex.substr(1, 2), 16);
                rgb[1]=parseInt(hex.substr(3, 2), 16);
                rgb[2]=parseInt(hex.substr(5, 2), 16);
                return rgb;
            } catch (e) {
                throw e;
            }
        }

        //generates the hex-digits for a color. 
        function hex(x) {
            return isNaN(x) ? "00" : hexDigits[(x - x % 16) / 16] + hexDigits[x % 16];
        }
        
        // checks, if an array of three values is a valid rgb-array
        function checkRGB(rgb) {
             if (rgb.length!=3) throw "this is not a valid rgb-array";
             if (isNaN(rgb[0]) || isNaN(rgb[1]) || isNaN(rgb[2])) throw "this is not a valid rgb-array";
             if (rgb[0]<0 || rgb[0]>255 || rgb[1]<0 || rgb[1]>255 || rgb[2]<0 || rgb[3]>255) throw "this is not a valid rgb-array";
             return rgb;
        }
        
        // generates a hex value, using a rgb value
        function rgb2hex(rgb) {
            try {
                checkRGB(rgb);
                return "#" + hex(rgb[0]) + hex(rgb[1]) + hex(rgb[2]);
            } catch (e) {
                throw e;
            }
        }
        
        //compares two values to sort
        function cmp(a, b) {
            return a - b;
        }
        
        /**
         * calculateGradient for a color
         * @param startVal
         * @param endVal
         * @param count
         * @param type: array for each color. Speciefies, how the missing color should be calculated:
                                             1: linear
                                             2: trigonometrical 
                                             3: accidentally
                                             4: ordered accident
         */
         function calculateGradient(startVal, endVal, count, type) {
             var a = new Array();
             if(!type || !count) {
                 return null;
             } else if (1<count && count < 3) {
                 a[0] = startVal;
                 a[1] = endVal;
                 return a;
             } else if (count==1) {
                 a[0] = endVal;
                 return a;
             }
             
             switch(type) {
                 case 1: //"linear"
                     var i;
                     for(i = 0; i < count; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * i / (count - 1));
                     break;
         
                 case 2: //trigonometrical 
                     var i;
                     for(i = 0; i < count; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * ((Math.sin((-Math.PI / 2) + Math.PI * i / (count - 1)) + 1) / 2));
                     break;
         
                 case 3: //accident
                     var i;
                     for(i = 1; i < count - 1; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * Math.random());
                     a[0]    = startVal;
                     a[count - 1]    = endVal;
                     break;
         
                 case 4: //ordered accident
                     var i;
                     for(i = 1; i < count - 1; i++)
                         a[i] = Math.round(startVal + (endVal - startVal) * Math.random());
                     a[0]    = startVal;
                     a[count - 1]    = endVal;
                     if((typeof(a.sort) == "function") && (typeof(a.reverse) == "function"))
                     {
                         a.sort(cmp);
                         if(startVal > endVal)
                             a.reverse();
                     }
                     break;
             }
             return a;
         }
    
        /**
        * calculates an array with hex values. 
        * @param startColor: starting color (hex-format or rgb)
        * @param endColor: ending color (hex-format or rgb)
        * @param count: specifies, how many colors should be generated
        * @params types: array for each color.
        *         Speciefies, how the missing color should be calculated:
        *               1: linear
        *               2: trigonometrical 
        *               3: accidentally
        *               4: ordered accident
        */
        function calculateColor(startColor, endColor, count, types) {
            if(!types || types.length != 3) {
                types = [1,1,1];
            }
            var start,end,
                rgb = [],
                color = [];
            try {
                try {
                    start   = hex2rgb(startColor);
                    end     = hex2rgb(endColor);
                } catch (e) {
                    //no hex-value => check if rgb
                    checkRGB(startColor);
                    start = startColor;
                    checkRGB(endColor);
                    end = endColor;
                }
                
                rgb[0]  = calculateGradient(start[0], end[0], count, types[0]);
                rgb[1]  = calculateGradient(start[1], end[1], count, types[1]);
                rgb[2]  = calculateGradient(start[2], end[2], count, types[2]);
            
                for(var i = 0; i < count; i++) {
                    color[i] = "#" + hex(rgb[0][i]) + hex(rgb[1][i]) + hex(rgb[2][i]);
                }
            } catch (e) {
                throw e;
            }
            return color;
        }
        
        return calculateColor;
    }());
    
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

    $.ecoplot = (function() {
        
        function console_logger(msg) {
            if (typeof console !== "undefined" && typeof console.debug !== "undefined") {
                console.log(msg);
            }
        }
        
        var _version = "@VERSION",
            plugin_class = "econometric-plot",
            extraTools     = {},
            events         = {},
            menubar		   = {},
            debug		   = false,
            css_loaded	   = false,
            siteoptions	   = {
                url: null,
                theme: 'smooth'
            },
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
            default_toolbar = [
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
                   classname: 'toggle-legend',
                   title: "Toggle legend",
                   icon: "ui-icon-comment",
                   type: "checkbox",
                   decorate: function(b,el) {
                       var $this = $(el);
                       b.toggle(function() {
                            $('.legend',el).hide();
                        },
                        function() {
                            $('.legend',el).show();
                        }
                      );
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
               ],
           defaults = {
               responsetype:   'json',
               requestMethod:  'get',
               url: null,
               autoload: true,
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
               toolbar: default_toolbar,
               commandline: default_command_line,
               showplot: function(i) {return true;},
               requestParams: {},
               show_tooltip: true,
               loaderimage: 'ajax-loader.gif',
               flot_options: {
                   xaxis: {}
               },
               paginate: null,
               infoPanel: 'ecoplot-info',
               min_height: 200,
               defaultFade: 300,
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
           

        function showPanel(p,el) {
            $('.secondary .panel').hide();
            if(p) {
                el.options.elems.body.addClass('with-panel');
                p.show();
            }
            if(el.options.canvases) {
                el.options.canvases.render();
            }
        }
        
        function hidePanel(name,el) {
            $('.secondary .panel').hide();
            el.options.elems.body.removeClass('with-panel');
            if(el.options.canvases) {
                el.options.canvases.render();
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
        function _registerEvents($this) {
            var opt = $this[0].options;
            var elems = opt.elems;

            $(window).resize(function() {
                if(opt.canvases) {
                    opt.canvases.render();
                }
            });

            $.each(events, function(id,eve) {
                $.ecoplot.log.debug('Registering event '+id);
                eve.register($this);
            });
        }

        function _get_data($this)  {
            var elems = $this[0].options.elems,
                ticker = elems.commandline.val();
            if(!ticker) {return null;}
            return {
                start: elems.dates.start.val(),
                end: elems.dates.end.val(),
                period:'',
                command:ticker
            };
        }

        /**
         * Create the editing panel for a given Flot canvas
         */
        function _editpanel(data, showplot, oldcanvas) {
            // check if oldcanvas is the same. If so keep it!
            var newcanvas = data,
                table = null,
                body  = null,
                oldbody = null,
                oseries = [];
            if(!oldcanvas) {
                $.ecoplot.log.debug('Creating editing panel.');
                table = $('<table class="plot-options"></table>');
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
            $.ecoplot.log.debug('Adding '+ typ + ' data to flot canvases.');
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
         * Internal function for setting up one or more new flot plot depending on data.
         * It creates the options.canvases object of the form:
         * 
         * options.canvases = {
         *      all: Array of canvases
         *      height: height of canvas
         *      current: index of current canvas or null
         *      }
         * 
         * @param $this jQuery ecoplot element
         * @params data Json data
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
                // create options panel if not available
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
            var options  = $this[0].options,
                log = $.ecoplot.log;
            if(!options.url)  {return;}
            var dataplot = _get_data($this);
            if(!dataplot) {return;}
            log.info("Sending ajax request to " + options.url);
            log.debug(dataplot.command + ' from ' + dataplot.start + ' end '+ dataplot.end);
            var params   = {
                    timestamp: +new Date()
            };
            $.each(options.requestParams, function(key, param) {
                params[key] = typeof param === "function" ? param() : param;
            });
            params = $.extend(true, params, dataplot);
            options.startLoading($this);
            $.ajax({url: options.url,
                type: options.requestMethod,
                data: $.param(params),
                dataType: options.responsetype,
                success: function(data) {
                    log.info("Got the response from server");
                    var ok = true;
                    if(options.parse)  {
                        try {
                            data = options.parse(data,$this);
                        }
                        catch(e) {
                            ok = false;
                            log.error("Failed to parse. Error in line ",e);
                        }
                    }
                    options.stopLoading($this);
                    if(ok)  {
                        try {
                            _finaliseLoad($this,data);
                        }
                        catch(e2) {
                            log.error("Failed after data has loaded",e2);
                        }
                    }
                }
            });
        }

        /**
         * The jQuery plugin constructor
         */
        function _construct(options_) {
            var options = _parseOptions(options_);
            return this.each(function(i) {
                
                var $this = $(this).attr({'id':plugin_class+"_"+i}).addClass(plugin_class);
                this.options = options;
                $this.hide().html("");
                options.paginate($this);
                
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
        return {
            construct: _construct,
            loadData: _request,
            addEvent: function(e){_addelement(e,events);},
            removeEvent: function(id){delete events[id];},
            debug: function(){return debug;},
            setdebug: function(v){debug = v;},
            log: default_logger,
            version: _version,
            'plugin_class': plugin_class,
            addMenu: function(menu) {menubar[menu.name] = menu;},
            getmenu: function(name,$this) {
                var menu = menubar[name];
                if(menu) {
                    return menu.create($this[0]);
                }
            }
        };
    }());



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
                if(ax.xaxis)  {
                    opts.xaxis = checkax(ranges.xaxis);
                }
                if(ax.yaxis)  {
                    opts.yaxis = checkax(ranges.yaxis);
                }
                if(ax.x2axis)  {
                    opts.x2axis = checkax(ranges.x2axis);
                }
                if(ax.y2axis)  {
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

}(jQuery));
