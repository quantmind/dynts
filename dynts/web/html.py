from djpcms import html


def sparkline(data, **options):
    return  html.Widget('span', cn = 'sparkline')\
                .addData('data',data)\
                .addData('options',options)