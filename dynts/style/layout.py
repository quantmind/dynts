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
           data = {'padding':'2px',
                   'font_size':'90%'}
           )

CssContext('ecolegend',
           tag = '.ecolegend',
           data = {'font_size':'90%'}
           )

CssContext('ts-input-date',
           tag = '.ts-input-date',
           data = {'margin':'0',
                   'padding':'4px',
                   'width':'90px'}
           )

CssContext('ecoplot-secondary',
           tag = '.secondary',
           parent = ecoplot,
           data = {'overflow':'auto'},
           elems = [
            CssContext('ecoplot-secondary-panel',
                tag = '.panel',
                data = {'padding': '10px'}
                )
        ]
    )

CssContext('ecoplot_plot_options',
           tag = '.plot-options',
           data = {'font_size':'90%'},
           elems = [
            CssContext('ecoplot_plot_options_header',
                tag = 'th',
                data = {'font_weight':'bold'}
                ),
            CssContext('ecoplot_plot_options_body',
                tag = 'td',
                data = {'font_weight':'normal'}
                ),
            CssContext('ecoplot_plot_options_input',
                tag = 'input',
                data = {'margin':'0'}
                ),
            CssContext('ecoplot_plot_options_input_tiny',
                tag = 'input.tiny',
                data = {'width': '1em'}
                ),
            CssContext('ecoplot_plot_options_toggle',
                tag = '.ui-button-text-only .ui-button-text',
                data = {
                    'padding': '0 0.5em'}
                ),
            CssContext('ecoplot_plot_serie_title',
                tag = 'tr.serie-title td',
                data = {'font_size': '100%',
                        'text_align':'left',
                        'font_weight':'bold',
                        'padding': '5px 5px 0'}
                ),
            CssContext('ecoplot_plot_serie_options',
                tag = 'tr.serie-option td',
                data = {'padding': '0 5px'}
                )
        ]
)

CssContext('ecoplot_plot_options_cells',
           tag = '.plot-options th, .plot-options td',
           data = {
                'padding': '0 5px',
                'text_align': 'center',
                'vertical_align': 'middle'}
           )
