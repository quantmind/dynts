from djpcms import html, media

SPARKLINE_MEDIA = ['dynts/jquery.sparkline.js',
                   'dynts/decorator.js']

FLOT_MEDIA = media.Media(js = ['dynts/flot/excanvas.min.js',
                              'dynts/flot/jquery.flot.js',
                              'dynts/flot/jquery.flot.selection.js',
                              'dynts/jquery.flot.text.js',
                              'dynts/base64.js',
                              'dynts/canvas2image.js',
                              'dynts/ecoplot/ecoplot.js']+\
                              SPARKLINE_MEDIA)

sparkline_maker = html.WidgetMaker(
                    tag = 'span',
                    default_class = 'sparkline',
                    media = FLOT_MEDIA)

def sparkline(data, **options):
    return  html.Widget(sparkline_maker)\
                .addData('data',data)\
                .addData('options',options)