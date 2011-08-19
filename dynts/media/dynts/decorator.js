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
        
        var sparkline_decorator = function (elem,config) {
            $.each($('.sparkline',elem),function() {
                var v = $(this),
                    data = v.data(),
                    serie = data.data,
                    options = data.options;
                if(serie) {
                    v.sparkline(serie,options);
                }
            });
        };
        
        $.djpcms.decorator({
            id:"sparkline",
            config: {},
            decorate: sparkline_decorator
        });

        if(!$.djpcms.options.datatable) {
            $.djpcms.options.datatable = {fnRowCallbacks:[]};
        }

        $.djpcms.options.datatable.fnRowCallbacks.push(
            function(nRow, aData, iDisplayIndex, iDisplayIndexFull){
                sparkline_decorator(nRow);
            });
    }
    
    if($.plot) {
            
        $.djpcms.decorator({
            id:"econometric_plot",
            decorate: function(elem,config) {
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
                
                $(selector,elem).each(function() {
                    var start,
                        el = $(this),
                        options = el.data();
                    options.jsondata.parse = parsedata;
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
