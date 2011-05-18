from medplate import CssContext

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
                       'width':'100%',
                       }
            )
    
    CssContext('ecoplot_body',
               tag = '.body',
               parent = ecoplot,
               data = {'border':'none'
                }
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
    