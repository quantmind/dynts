# -*- coding: utf-8 -*-
import csv

from io import BytesIO as StreamIO

try:
    from itertools import izip as zip
except ImportError:
    pass

from dynts.exceptions import FormattingException
from dynts.backends import istimeseries
from dynts.utils import asarray

default_converter = lambda x : x.isoformat()


def tsiterator(ts, dateconverter = None, desc = None):
    dateconverter = dateconverter or default_converter
    yield ['Date']+ts.names()
    for dt,value in ts.items(desc = desc):
        dt = dateconverter(dt)
        yield [dt]+list(value)


class BaseFormatter(object):
    type = None
    default = False


class ToCsv(BaseFormatter):
    type = 'csv'
    
    def __call__(self, ts, filename = None, **kwargs):
        '''Returns CSV representation of a :class:`dynts.TimeSeries`.'''
        stream = StreamIO()
        _csv = csv.writer(stream)
    
        for row in tsiterator(ts):
            _csv.writerow(row)
    
        return stream.getvalue()


class ToFlot(BaseFormatter):
    type = 'json'
    default = True
    def __call__(self, ts, container = None, desc = False, series_info = None, **kwargs):
        '''Dump timeseries as a JSON string compatible with ``flot``'''
        from dynts.web import flot
        from dynts.conf import settings
        
        pydate2flot = flot.pydate2flot
        result = container or flot.MultiPlot()
        df = {}
        series_info = series_info or df
        if istimeseries(ts):
            res = flot.Flot(ts.name, type = 'timeseries', **series_info)
            dates  = asarray(ts.dates())
            missing = settings.ismissing
            for name,serie in zip(ts.names(),ts.series()):
                info = series_info.get(name,df) 
                data = []
                append = data.append
                for dt,val in zip(dates,serie):
                    if not missing(val):
                        append([pydate2flot(dt),val])
                serie = flot.Serie(label = name, data = data, **info)
                res.add(serie)
        else:
            res = flot.Flot(ts.name)
            for name,serie in zip(ts.names(),ts.series()):
                serie = flot.Serie(label = serie.name,
                                   data = serie.data,
                                   lines = {'show':serie.lines},
                                   points = {'show':serie.points})
                res.add(serie)
        result.add(res)
        return result


class ToJsonVba(BaseFormatter):
    '''A JSON Formatter which can be used to serialize data to
VBA. For unserializing check http://code.google.com/p/vba-json/

The unserializer is also included in the directory extras'''
    type = 'json'
    def __call__(self, ts, container = None, desc = False, **kwargs):
        '''Dump timeseries as a JSON string VBA-Excel friendly'''
        from ccy import date2juldate
        from dynts.utils.anyjson import JSONdatainfo
        if istimeseries(ts):
            return JSONdatainfo(list(tsiterator(ts, dateconverter=date2juldate, desc = desc)),
                                info = ts.info)
        else:
            raise NotImplementedError


class ToXls(BaseFormatter):
    type = 'xls'
    
    def __call__(self, ts, filename = None, title = None, raw = False, **kwargs):
        '''Dump the timeseries to an xls representation.
This function requires the python xlwt__ package.
    
__ http://pypi.python.org/pypi/xlwt'''
        try:
            import xlwt
        except ImportError:
            raise FormattingException('To save the timeseries as a spreadsheet, the xlwt python library is required.')
        
        
        if isinstance(filename,xlwt.Workbook):
            wb = filename
        else:
            wb = xlwt.Workbook()
        title = title or ts.name
        stream = StreamIO()
        sheet = wb.add_sheet(title)
        for i,row in enumerate(tsiterator(ts)):
            for j,col in enumerate(row):
                sheet.write(i,j,str(col))
        
        if raw:
            return wb
        else:
            stream = StreamIO()
            wb.save(stream)
            return stream.getvalue()
    

class ToPlot(BaseFormatter):
    type = 'python'
       
    def __call__(self, ts, **kwargs):
        try:
            import tsplot
            return tsplot.toplot(ts, **kwargs)
        except ImportError:
            raise FormattingException('To plot timeseries, matplotlib is required.')
    
    
            
        