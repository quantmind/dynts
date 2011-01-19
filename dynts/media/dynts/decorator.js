/**
 * Decorator function for djpcms
 * See http://github.com/lsbardel/djpcms
 * 
 */

(function($) {
    
    var dj = $.djpcms;
    
    $.start_ecoplot = function(elem,poptions,parsedata) {
    	$(".econometric-plot",elem).each(function() {
    		var start;
    		var el   = $(this);
    		var url  = $('a',el).attr('href');
    		var height = parseInt($('.height',el).html());
    		try {
    			start  = parseInt($('.start',el).html());
    			start  = new Date(start);
    		}
    		catch(e) {
    			start = null;
    		}
    		var item = $('.item',el);
    		var dshow = $('.show',el);
    		el.height(height);
    		var cmline;
    		if(item.length) {
    			cmline = {
    				symbol: item.html(),
    				show: false
    			};
    		}
    		else {
    			cmline = null;
    		}
    		el.html('');
    		var info = $(".server-logger");
    		var elems_ = null;
    		if(info) {
    			elems_ = {'info': info};
    		}
    		var options = {
        			load_url:		url,
        			commandline:    cmline,
        			elems:		    elems_,
        			flot_options:   poptions,
        			parse: 		    parsedata,
        			start:			start,
        			height:			height,
        		}; 
    		if(!dshow.length) {
    			options.showplot = function(i) {return i<=1;}
    		}

    		el.ecoplot(options);
    	});
    }

    /**
     * DJPCMS Decorator for Econometric ploting
     */
    dj.addDecorator({
        id:"econometric_plot",
        decorate: function($this,config) {
    		function parse(data,el) {
				var res = data.result;
				if(res.type == 'multiplot') {
					return res.plots;
				}
			}
    		
            var poptions = {
                    colors: ["#205497","#2D8633","#B84000","#d18b2c"],
                    grid: {hoverable: true, clickable: true, color: '#00264D', tickColor: '#A3A3A3'},
                    selection: {mode: 'xy', color: '#3399FF'},
                    lines: {show: true, lineWidth: 3},
                    shadowSize: 0
            };
            
            $.start_ecoplot($this,poptions,parse);
        }
    });
    

})(jQuery);
