from djpcms import html
from djpcms.utils import media

SPARKLINE_MEDIA = media.Media(js = ['dynts/jquery.sparkline.js',
                                    'dynts/decorator.js'])

sparkline_maker = html.WidgetMaker(
                    tag = 'span',
                    default_class = 'sparkline',
                    media = SPARKLINE_MEDIA)

def sparkline(data, **options):
    return  html.Widget(sparkline_maker)\
                .addData('data',data)\
                .addData('options',options)