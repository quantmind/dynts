import csv
from io import StringIO


class Formatter:
    type = None
    default = False


class ToCsv(Formatter):
    type = 'csv'

    def __call__(self, ts, filename=None, **kwargs):
        stream = StringIO()
        _csv = csv.writer(stream)

        for row in tsiterator(ts):
            _csv.writerow(row)

        return stream.getvalue()


def tsiterator(ts, dateconverter=None, desc=None,
               clean=False, start_value=None, **kwargs):
    '''An iterator of timeseries as tuples.'''
    dateconverter = dateconverter or default_converter
    yield ['Date'] + ts.names()
    if clean == 'full':
        for dt, value in full_clean(ts, dateconverter, desc, start_value):
             yield (dt,) + tuple(value)
    else:
        if clean:
            ts = ts.clean()
        for dt, value in ts.items(desc=desc, start_value=start_value):
            dt = dateconverter(dt)
            yield (dt,) + tuple(value)


def default_converter(x):
    return x.isoformat()


def nanvalue(value):
    for v in value:
        if v != v:
            return True


def full_clean(ts, dateconverter, desc, start_value):
    for dt, value in ts.items(desc=desc, start_value=start_value):
        dt = dateconverter(dt)
        value = tuple(value)
        if nanvalue(value):
            continue
        yield dt, value
