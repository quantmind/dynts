# -*- coding: utf-8 -*-
import cStringIO
import csv
from itertools import izip

from dynts.exceptions import FormattingException
from dynts.backends import istimeseries
from dynts.utils import asarray

default_converter = lambda x : x.isoformat()


def tsiterator(ts, dateconverter = None):
    dateconverter = dateconverter or default_converter
    yield ['Date']+ts.names()
    for dt,value in ts.items():
        dt = dateconverter(dt)
        yield [dt]+list(value)


class BaseFormatter(object):
    type = None
    default = False


class ToCsv(BaseFormatter):
    type = 'csv'
    
    def __call__(self, ts, filename = None, **kwargs):
        '''Returns CSV representation of a :class:`dynts.TimeSeries`.'''
        stream = cStringIO.StringIO()
        _csv = csv.writer(stream)
    
        for row in tsiterator(ts):
            _csv.writerow(row)
    
        return stream.getvalue()


class ToFlot(BaseFormatter):
    type = 'json'
    default = True
    def __call__(self, ts, **kwargs):
        '''Dump timeseries as a JSON string compatible with ``flot``'''
        from dynts.web import flot
        from dynts.conf import settings
        res = flot.Flot()
        result = flot.MultiPlot(res)
        dates  = asarray(ts.dates())
        missing = settings.ismissing
        for name,serie in izip(ts.names(),ts.series()):
            data = []
            for dt,val in izip(dates,serie):
                if not missing(val):
                    data.append([flot.pydate2flot(dt),val])
            serie = flot.Serie(label = name, data = data)
            res.add(serie)
        return result


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
        stream = cStringIO.StringIO()
        sheet = wb.add_sheet(title)
        for i,row in enumerate(tsiterator(ts)):
            for j,col in enumerate(row):
                sheet.write(i,j,str(col))
        
        if raw:
            return wb
        else:
            stream = cStringIO.StringIO()
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
    
    
            
        