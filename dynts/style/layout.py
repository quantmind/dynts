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


#CssContext('ecoplot_options',
#           parent = ecoplot,
#         )




