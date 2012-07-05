/**
 * Decorator function for djpcms
 * 
 * @requires djpcms 0.9
 * 
 * See http://github.com/lsbardel/djpcms
 * 
 */

(function($) {
    /**
     * DJPCMS Decorator for Econometric ploting
     */    
    if($.fn.sparkline) {
        
    	$.djpcms.decorator({
    		id: "sparkline",
            config: {
            	selector: '.sparkline'
            },
            decorate: function(elem,config) {
            	var opts = config.sparkline;
            	$.each($(opts.selector,elem),function() {
	                var v = $(this),
	                    data = v.data(),
	                    serie = data.data,
	                    options = data.options;
	                if(serie) {
	                    v.sparkline(serie,options);
	                }
	            });
            }
        });
    	
    }


    if($.plot) {
            
        $.djpcms.decorator({
            id:"econometric_plot",
            decorate: function(elem, config) {
        		$.ecoplot.log = $.djpcms.logger;
                var poptions = {
                        // colors: ["#205497","#2D8633","#B84000","#d18b2c"],
                        grid: {hoverable: true, clickable: true,
                                color: '#00264D', tickColor: '#A3A3A3'},
                        selection: {mode: 'xy', color: '#3399FF'},
                        lines: {show: true, lineWidth: 3},
                        shadowSize: 0
                    },
                    selector = '.'+$.ecoplot.plugin_class,
                    parsedata = function(data,instance) {
                        var res = data.result;
                        if(!res) {
                            res = data;
                        }
                        if(res.type === 'multiplot') {
                            return res.plots;
                        }
                    };
                    
                function errorback(data,instance) {
                    $.djpcms.jsonParse(data,instance.container());
                }
                
                $(selector,elem).each(function() {
                    var start,
                        el = $(this),
                        options = el.data();
                    options.ui = $.djpcms.ui;
                    options.ui.name = 'djpcms';
                    options.jsondata.parse = parsedata;
                    options.jsondata.errorcallbacks = [errorback];
                    options.flot_options = poptions;
                    options.showplot = function(i) {
                        return i<=1;
                    };
                    el.ecoplot(options);
                });
            }
        });
    }
    
}(jQuery));
