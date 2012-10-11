# -*- coding: utf-8 -*-
import csv

from dynts.utils.py2py3 import zip, StreamIO
from dynts.exceptions import FormattingException
from dynts.backends import istimeseries
from dynts.utils import asarray
from dynts.tsweb import flot
from dynts.conf import settings


default_converter = lambda x : x.isoformat()


def nanvalue(value):
    for v in value:
        if v != v:
            return True

def full_clean(ts, dateconverter, desc):
    for dt, value in ts.items(desc=desc):
        dt = dateconverter(dt)
        value = tuple(value)
        if nanvalue(value):
            continue
        yield dt, value

def tsiterator(ts, dateconverter=None, desc=None,
               clean=False, **kwargs):
    '''An iterator of timeseries as tuples.'''
    dateconverter = dateconverter or default_converter
    yield ['Date'] + ts.names()
    if clean == 'full':
        for dt, value in full_clean(ts, dateconverter, desc):
             yield (dt,) + tuple(value)
    else:
        if clean:
            ts = ts.clean()
        for dt, value in ts.items(desc=desc):
            dt = dateconverter(dt)
            yield (dt,) + tuple(value)
        

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

class ToExcel(BaseFormatter):
    type = 'excel'

    def __call__(self, ts, filename = None, **kwargs):
        '''Returns Excel representation of a :class:`dynts.TimeSeries`.'''
        rtn = []

        for row in tsiterator(ts):
            rtn.append(row)

        return rtn


class ToFlot(BaseFormatter):
    type = 'json'
    default = True

    def __call__(self, ts, container=None, desc=False, ordering=None,
                 series_info=None, **kwargs):
        '''Dump timeseries as a JSON string compatible with ``flot``'''
        pydate2flot = flot.pydate2flot
        result = container or flot.MultiPlot()
        series_info = self.get_serie_info(series_info)
        if istimeseries(ts):
            res = flot.Flot(ts.name, type='timeseries', **series_info)
            dates  = asarray(ts.dates())
            missing = settings.ismissing
            for name,serie in ts.named_series(ordering):
                info = self.get_serie_info(series_info,name)
                data = []
                append = data.append
                for dt,val in zip(dates,serie):
                    if not missing(val):
                        append([pydate2flot(dt),val])
                serie = flot.Serie(label = name, data = data, **info)
                res.add(serie)
        else:
            res = flot.Flot(ts.name)
            if ts.extratype:
                for name,serie in zip(ts.names(),ts.series()):
                    serie = flot.Serie(label = serie.name,
                                       data = serie.data,
                                       lines = {'show':serie.lines},
                                       points = {'show':True},
                                       scatter = {'show':serie.points},
                                       extratype = ts.extratype)
                    res.add(serie)
            else:
                for name,serie in zip(ts.names(),ts.series()):
                    serie = flot.Serie(label = serie.name,
                                       data = serie.data,
                                       lines = {'show':serie.lines},
                                       points = {'show':serie.points})
                    res.add(serie)
        result.add(res)
        return result

    def get_serie_info(self, serie_info, name = None):
        if not name:
            return series_info or {}
        else:
            return series_info.get(name,{})


class ToJsonVba(BaseFormatter):
    '''A JSON Formatter which can be used to serialize data to
VBA. For unserializing check http://code.google.com/p/vba-json/

The unserializer is also included in the directory extras'''
    type = 'json'
    def __call__(self, ts, container = None, **kwargs):
        '''Dump timeseries as a JSON string VBA-Excel friendly'''
        from ccy import date2juldate
        from dynts.utils.anyjson import JSONdatainfo
        if istimeseries(ts):
            return list(tsiterator(ts, dateconverter=date2juldate, **kwargs))
        else:
            raise NotImplementedError()


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



