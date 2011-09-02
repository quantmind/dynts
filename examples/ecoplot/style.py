from medplate import CssBody, CssContext, CssTheme

CssBody()


CssContext('footer',
           tag = '#page-footer',
           data = {
            'overflow':'hidden',
            'min-height':'200px',
            'font_size':'90%',
            'padding':'20px 0 0'
            }
        )

CssContext('page-header',
           tag = '#page-header')

CssContext('geo-entry',
           tag = '.geo-entry',
           data = {
            'padding':'7px',
            'margin':'0 0 20px 0'
            },
            elems = [CssContext('geo-entry-def',
                        tag = '.object-definition',
                        data = {
                            'margin':'0'
                        })
                     ]
            )
CssContext('jslog',
           data = {
            'height':'200px'
        }
)


#_____________________________________ THEMES

CssTheme('page-header',
         'smooth',
         data = {
            'background':'#ccc'
        })
