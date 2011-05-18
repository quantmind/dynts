from .lfunc import *

ecoplot = CssContext('ecoplot',
                     tag = '.econometric-plot',
                     template = 'dynts/ecoplot.css_t',
                     data = {'line_height':'25px',
                             'overflow':'hidden'
                        }
                     )

MakeUpperMenu(ecoplot,
              height = 40,
              vertical_margin_input = 4)


CssContext('ecoplot_tooltip',
           tag = '.econometric-plot-tooltip',
           data = {'padding':'2px'}
           )

CssContext('ecoplot_legend',
           tag = '.econometric-plot .legend',
           data = {'padding':'10px'}
           )

CssContext('ecoplot_secondary',
           tag = '.secondary .panel',
           parent = ecoplot,
           data = {'padding': '10px'}
           )

CssContext('ecoplot_plot_options',
           tag = 'table.plot-options th, table.plot-options td',
           parent = ecoplot,
           data = {'padding': '0 5px',
                   'text_align': 'center'}
           )


