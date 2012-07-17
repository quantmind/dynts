'''Styling for ecoplot javascript plugin.
Make sure "djpcms.apps.ui" is included before "dynts.tsweb"
in the INSTALLED_APPS list.'''
from djpcms.media.style import *
from djpcms.forms.layout import classes

from .html import appname

cssv.ecoplot.padding = px(10)
cssv.ecoplot.dateinput.width = px(90)

cssv.ecoplot.legend.background = cssv.widget.body.background
cssv.ecoplot.legend.color = cssv.widget.body.color
cssv.ecoplot.legend.border.color = cssv.widget.border.color

cssv.ecoplot.tooltip.background = cssv.ecoplot.legend.background
cssv.ecoplot.tooltip.color = cssv.ecoplot.legend.color
cssv.ecoplot.tooltip.border.color = cssv.ecoplot.legend.border.color


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
            cssb('label.%s' % classes.button, margin=0),
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
    css('.main',
        width=pc(100),
        height=pc(100),
        float='left'),
    css('.secondary',
        css('.panel',
            padding='10px'),
        width=pc(100),
        height=pc(100),
        float='right'),
    css('.with-panel',
        css('.main,.secondary',
            width=pc(50))),
    overflow='hidden')

css('.econometric-plot-tooltip',
    gradient(cssv.ecoplot.tooltip.background),
    border(**cssv.ecoplot.tooltip.border.params()),
    padding='2px',
    color=cssv.ecoplot.tooltip.color,
    font_size='90%')

css('.ecolegend',
    gradient(cssv.ecoplot.legend.background),
    border(**cssv.ecoplot.legend.border.params()),
    color=cssv.ecoplot.legend.color,
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

css('.econometric-plot',
    css('.loader',
        opacity(0.5),
        image('%s/ecoplot/img/ajax-loader.gif' % appname),
        display='none',
        height=px(30),
        float='right',
        width=px(30)))

css('.plot-options th, .plot-options td',
    padding='0 5px',
    text_align='center',
    vertical_align='middle')