import os
from djpcms import html, media

appname = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

SPARKLINE_MEDIA = ['%s/jquery.sparkline.js'%appname,
                   '%s/decorator.js'%appname]

FLOT_MEDIA = media.Media(js = ['%s/flot/excanvas.min.js'%appname,
                               '%s/flot/jquery.flot.js'%appname,
                               '%s/flot/jquery.flot.selection.js'%appname,
                               '%s/jquery.flot.text.js'%appname,
                               '%s/base64.js'%appname,
                               '%s/canvas2image.js'%appname,
                               '%s/jquery.ba-resize.js'%appname,
                               '%s/ecoplot/ecoplot.js'%appname]+\
                               SPARKLINE_MEDIA)

sparkline_maker = html.WidgetMaker(
                    tag='span',
                    default_class='sparkline',
                    media=FLOT_MEDIA)

def sparkline(data, **options):
    return  html.Widget(sparkline_maker)\
                .addData('data', data)\
                .addData('options', options)