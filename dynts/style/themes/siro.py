from djpcms.style import CssTheme

theme_name = 'siro'
body = '#E8EDF0'
dark = '#353432'
light = '#DCDCDC'


CssTheme(('ecoplot_tooltip','ecoplot_legend'),
         theme_name,
         data = {
                 'background': '#9CC4E4',
                 'border': '1px solid #1B325F',
                 'opacity': '0.7'
                 }
         )