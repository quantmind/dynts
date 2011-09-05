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
                $('.color',nRow).each(function() {
                    var el = $(this),
                        val = el.html();
                    try {
                        val = parseFloat(val);
                        if(val < 0) {
                            el.addClass('ui-state-error-text');
                        }
                        if(el.hasClass('arrow') && val === val) {
                            var ar = $('<span></span>').css({'margin-right':'.3em',
                                                         'float':'right'});
                            val > 0 ? ar.addClass('ui-icon ui-icon-arrowthick-1-n') :
                                      ar.addClass('ui-icon ui-icon-arrowthick-1-s');
                            el.append(ar);
                        }
                    }catch(e){}
                });
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
                    
                function errorback(data,instance) {
                    $.djpcms.jsonParse(data,instance.container());
                }
                
                $(selector,elem).each(function() {
                    var start,
                        el = $(this),
                        options = el.data();
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
