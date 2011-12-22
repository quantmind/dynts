from djpcms import html
from djpcms.utils import media

sparkline_maker = html.WidgetMaker(
                    tag = 'span',
                    default_class = 'sparkline',
                    media = media.Media(js = ['dynts/jquery.sparkline.js',
                                              'dynts/decorator.js']))

def sparkline(data, **options):
    return  html.Widget(sparkline_maker)\
                .addData('data',data)\
                .addData('options',options)