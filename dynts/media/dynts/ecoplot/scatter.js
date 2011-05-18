/**
 * TIMESERIE SCATTER PLOT PLUGIN FOR PLOT.
 * 
 * It allows to have different colors for points referring to different dates.
 */
(function($) {
    
    if($.plot) {
        
        $.plot.plugins.push((function() {
            
            var defaults = {
                series: {
                    scatter: {
                        radius: 5,
                        lineWidth: 1,
                        gradient: 1,
                        symbol: 'circle',
                    }
                }
            };
            
            function calculateColors(plot, series) {
                var opts = plot.getOptions(),
                    legend = opts.legend;
            }
            
            // Get the colour scheme for each point
            function scatter_colours(plot, series, datapoints) {
                if(!series.scatter){return;}
                var opts = plot.getOptions(),
                    data = series.data,
                    NC = opts.colors.length,
                    N = data.length,
                    S = Math.floor(N/(NC-1)),
                    scatter = opts.series.scatter,
                    colors = [],
                    minv,maxv,c,lv,dc,sdata,i;
                if(scatter.data) {return;}
                scatter.data = sdata = [];
                if(series.lines) {series.lines.show = false;}
                if(series.points) {series.points.show = false;}
                if(series.bars) {series.bars.show = false;}
                if(!N) {return;}
                scatter.colors = colors;
                if(S) {
                    for(i=1;i<NC;i++) {
                        if(i == NC-1) {
                            S = N - S*(NC-2);
                        }
                        $.each($.color_gradient(opts.colors[i-1],
                                                opts.colors[i],
                                                S,
                                                scatter.gradient),function(i,val) {
                            colors.push(val);
                        });
                    }
                }
                minv = maxv = data[0][2];
                $.each(data,function(i,v) {
                    lv = v[2];
                    minv = Math.min(minv,lv);
                    maxv = Math.max(maxv,lv);
                });
                $.each(data,function(i,v) {
                    lv = v[2];
                    c = (lv - minv)/(maxv - minv);
                    sdata.push(Math.floor(c*N));
                    if(lv === maxv) {scatter.last = i;}
                });
            }
            
            function gradient_div(colors) {
                var el = $('<div>').css({'padding':'1px'}),
                    i,c0,c1;
                for(i=1;i<colors.length;i++) {
                    c0 = colors[i-1];
                    c1 = colors[i];
                    $('<div>').width(10).height(20).appendTo(el)
                            .css({'background-color':c1,
                                  'background-image': '-moz-linear-gradient(top, '+c1+','+c0+')',
                                  'background-image': '-webkit-linear-gradient('+c1+','+c0+')',
                                  'background-image': 'linear-gradient(top, '+c1+','+c0+')'});
                }
                return el;
            }
            
            function drawSeries(plot, ctx, series) {
                var options = plot.getOptions(),
                    scatter = options.series.scatter,
                    colors = scatter.colors,
                    plotOffset = plot.getPlotOffset(),
                    points = options.series.scatter,
                    sw = options.series.shadowSize,
                    lw = points.lineWidth,
                    radius = points.radius,
                    symbol = points.symbol,
                    gradient = gradient_div(options.colors),
                    self = plot.getPlaceholder(),
                    legend = $('.legend',self),
                    table = $('table',legend); 
                
                if(!scatter) {return;}
                
                $('.legendColorBox',table).empty().append(gradient);
                legend.remove();
                legend = $('<div class="legend">').prependTo(self);
                legend.append($('<table>').html(table.html()));
                legend.draggable({containment:self});
                
                function fillcolor(i) {
                    return colors[scatter.data[i]];
                }
                
                function plotPoints(datapoints, radius, fillStyle, offset, shadow,
                                    axisx, axisy, symbol) {
                    var points = datapoints.points, ps = datapoints.pointsize;
                    
                    for(var i = 0; i < points.length; i += ps) {
                        var x = points[i], y = points[i + 1];
                        if (x == null || x < axisx.min || x > axisx.max || y < axisy.min || y > axisy.max)
                            continue;
                        
                        ctx.beginPath();
                        x = axisx.p2c(x);
                        y = axisy.p2c(y) + offset;
                        if (symbol == "circle")
                            ctx.arc(x, y, radius, 0, shadow ? Math.PI : Math.PI * 2, false);
                        else
                            symbol(ctx, x, y, radius, shadow);
                        ctx.closePath();
                        
                        if(fillStyle) {
                            ctx.fillStyle = fillcolor(i);
                            ctx.fill();
                        }
                        ctx.stroke();
                    }
                }
                
                ctx.save();
                ctx.translate(plotOffset.left, plotOffset.top);
    
                if (lw > 0 && sw > 0) {
                    // draw shadow in two steps
                    var w = sw / 2;
                    ctx.lineWidth = w;
                    ctx.strokeStyle = "rgba(0,0,0,0.1)";
                    plotPoints(series.datapoints, radius, null, w + w/2, true,
                               series.xaxis, series.yaxis, symbol);
                    ctx.strokeStyle = "rgba(0,0,0,0.2)";
                    plotPoints(series.datapoints, radius, null, w/2, true,
                               series.xaxis, series.yaxis, symbol);
                }
    
                ctx.lineWidth = lw;
                ctx.strokeStyle = series.color;
                plotPoints(series.datapoints, radius, fillcolor, 0, false,
                           series.xaxis, series.yaxis, symbol);
                ctx.restore();
            }
    
            function _init(plot) {
                plot.hooks.processDatapoints.push(scatter_colours);
                plot.hooks.drawSeries.push(drawSeries);
            }
            
            return {
                name: 'scatter',
                version: '0.1',
                init:_init,
                options: defaults
            };
        }()));
    
    }
    
}(jQuery));

