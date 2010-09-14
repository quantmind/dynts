# -*- coding: utf-8 -*-
import cStringIO
import csv

default_converter = lambda x : x.isoformat()

def tsiterator(ts, dateconverter = None):
    dateconverter = dateconverter or default_converter
    yield ['Date']+ts.names()
    for dt,value in ts.items():
        dt = dateconverter(dt)
        yield [dt]+list(value)

def tocsv(ts, filename = None, **kwargs):
    '''Returns CSV representation of a :class:`dynts.TimeSeries`.'''
    stream = cStringIO.StringIO()
    _csv = csv.writer(stream)

    for row in tsiterator(ts):
        _csv.writerow(row)

    return stream.getvalue()


def toflot(ts, **kwargs):
    pass