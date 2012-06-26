from djpcms.media.style import *


def MakeUpperMenu(ecoplot,
                  height = 36,
                  vertical_margin_input = 4,
                  vertical_padding_input = 4):
    '''Style the Ecoplot plugin header with a input command line,
dates inputs and the toolbar.
    '''
    h = '{0}px'.format(height)
    ih = height-2*(vertical_margin_input+vertical_padding_input)
    um = CssContext('ecoplot_menubar',
               tag = '.menubar',
               parent = ecoplot,
               data = {'height': h,
                       'line_height': h,
                       'float': 'left',
                       'width':'90%'
                       }
            )
    
    CssContext('ecoplot_body',
               tag = '.body',
               parent = ecoplot
               #data = {'border':'none'
               # }
               )
    
    CssContext('ecoplot_commandline',
               tag = '.menubar.upper input',
               parent = ecoplot,
               data = {
                    'height': '{0}px'.format(ih),
                    'margin': '{0}px 1%'.format(vertical_margin_input),
                    'padding': '{0}px 1%'.format(vertical_padding_input),
                    'width': '96%',
                    'border':'none'
                    }
               )

    CssContext('ecoplot_menuitem',
               tag = '.menu-item',
               parent = ecoplot,
               data = {'float': 'left',
                       'margin':'0 0 0 1%',
                       }
            )
    

css('.econometric-plot',
    css('.secondary',
        css('.panel',
            padding='10px'),
        overflow='auto'),
    line_height='25px',
    overflow='hidden')

#MakeUpperMenu(ecoplot,
#              height = 40,
#              vertical_margin_input = 4)


css('.econometric-plot-tooltip',
    padding='2px',
    font_size='90%')

css('ecolegend',
    font_size='90%')

css('.ts-input-date',
    margin=0,
    padding='4px',
    width='90px')

css('.plot-options',
    css('th', font_weight='bold'),
    css('td', font_weight='normal'),
    css('input',
        cssa('.tiny', width='1em'),
        margin=0),
    css('.ui-button-text-only .ui-button-text',
        padding= '0 0.5em'),
    css('tr.serie-title td',
        font_size='100%',
        text_align='left',
        font_weight='bold',
        padding='5px 5px 0'),
    css('tr.serie-option td',
        padding='0 5px'),
    font_size='90%'
)

css('.plot-options th, .plot-options td',
    padding='0 5px',
    text_align='center',
    vertical_align='middle')