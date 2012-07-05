from djpcms.media.style import *
from djpcms.forms.layout import classes

cssv.ecoplot.padding = px(10)
cssv.ecoplot.dateinput.width = px(90)


class uppermenu(mixin):
    '''Style the Ecoplot plugin header with a input command line,
dates inputs and the toolbar.
    '''
    def __call__(self, elem):
        height = cssv.ecoplot.menu.height
        css('.menu',
            cssb('*',
                 clearfix(),
                 float='left',
                 width=pc(100),
                 padding_bottom=cssv.ecoplot.padding.bottom),
            cssb('*:last-child', padding=0),
            parent=elem,
            padding=cssv.ecoplot.padding)
        
        css('.commandline',
            css('input',
                width=pc(100),
                padding=spacing(px(4), 0),
                outline='none',
                border='none'),
            parent=elem)
    
        css('.menu-item',
            cssb('*', float='left'),
            cssa(':last-child', margin=0),
            cssb('label',
                 cssa(':first-child', margin=spacing(0, px(5), 0, 0)),
                 margin=spacing(0, px(5))),
            parent=elem,
            float='left',
            margin=spacing(0, px(10), 0, 0))
        
        css('.dateholder',
            css('.%s'%classes.ui_input, width=cssv.ecoplot.dateinput.width))
        
        css('.loader',
            display='none',
            float='right')
    

css('.econometric-plot',
    uppermenu(),
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