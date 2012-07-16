/**
 * Decorator function for djpcms
 * 
 * @requires djpcms 0.9
 * 
 * See http://github.com/lsbardel/djpcms
 * 
 */
/*globals jQuery*/
(function ($) {
    "use strict";
    //
	$.djpcms.decorator({
	    name: "sparkline",
	    selector: '.sparkline',
	    config: {},
        _create: function () {
            if ($.fn.sparkline) {
                var serie = v.data('data');
                if (serie) {
                    this.element.sparkline(serie, this.config);
                }
            }
        }
    });
    //
    $.djpcms.decorator({
        name: "ecoplot",
        selector: '.econometric-plot',
        config: {
            classes: {},
            showplot: function (i) {
                return i <= 1;
            },
            flot_options: {
                grid: {
                    hoverable: true,
                    clickable: true,
                    color: '#00264D',
                    tickColor: '#A3A3A3'
                },
                selection: {
                    mode: 'xy',
                    color: '#3399FF'
                },
                lines: {
                    show: true,
                    lineWidth: 3
                },
                shadowSize: 0
            },
            jsondata: {
                parse: function (data, instance) {
                    var res = data.result;
                    if (!res) {
                        res = data;
                    }
                    if (res.type === 'multiplot') {
                        return res.plots;
                    }
                },
                errorcallbacks: [function (data, instance) {
                    $.djpcms.jsonParse(data, instance.container());
                }]
            }
        },
        _create: function () {
            if ($.ecoplot) {
                var options = this.config;
                $.ecoplot.log = $.djpcms.logger;
                options.ui = $.djpcms.ui;
                this.element.ecoplot(options);
            }
        }
    });
}(jQuery));