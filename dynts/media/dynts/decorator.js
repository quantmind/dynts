/**
 * Decorator function for djpcms
 * 
 * @requires djpcms 0.9
 * 
 * See http://github.com/lsbardel/djpcms
 * 
 */

(function($) {
    
    $.start_ecoplot = function(plugin_class,elem,poptions,parsedata) {
        $(".",elem).each(function() {
            var start;
            var elem = $(this);
            var options = elem.data();
            options.logger = $.djpcms.logger;
            options.parse = parsedata;
            options.flot_options = poptions;
    		options.showplot = function(i) {
			    return i<=1;
			};
    		el.ecoplot(options);
    	});
    };

    /**
     * DJPCMS Decorator for Econometric ploting
     */
    if($.djpcms) {
        $.djpcms.decorator({
            id:"econometric_plot",
            decorate: function($this,config) {
        		if(!$.ecoplot) {
        		    return;
        		}
                var poptions = {
                        // colors: ["#205497","#2D8633","#B84000","#d18b2c"],
                        grid: {hoverable: true, clickable: true, color: '#00264D', tickColor: '#A3A3A3'},
                        selection: {mode: 'xy', color: '#3399FF'},
                        lines: {show: true, lineWidth: 3},
                        shadowSize: 0
                    },
                    selector = '.'+$.ecoplot.plugin_class,
                    parse = function(data,el) {
                        var res = data.result;
                        if(res.type === 'multiplot') {
                            return res.plots;
                        }
                    };
                
                $(selector,elem).each(function() {
                    var start;
                    var elem = $(this);
                    var options = elem.data();
                    options.plugin_class = plugin_class;
                    options.logger = $.djpcms.logger;
                    options.parse = parsedata;
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
