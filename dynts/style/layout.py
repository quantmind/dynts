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

CssContext('ecoplot_secondary',
           tag = '.secondary .panel',
           parent = ecoplot,
           data = {'padding': '10px'}
           )

CssContext('ecoplot_plot_options',
           tag = 'table.plot-options th, table.plot-options td',
           data = {'padding': '0 5px'}
           )

CssContext('ecoplot_plot_serie_title',
           tag = 'table.plot-options tr.serie-title td',
           data = {'font_size': '120%',
                   'text_align':'left',
                   'font_weight':'bold',
                   'color':'#222',
                   'padding': '10px 5px 5px'}
           )

CssContext('ecoplot_plot_serie_options',
           tag = 'table.plot-options tr.serie-option td',
           data = {'padding': '0 5px 5px'}
           )

