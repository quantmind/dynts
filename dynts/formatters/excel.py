from io import StringIO

from .base import Formatter, tsiterator

try:
    import xlwt
except ImportError:
    xlwt = None


class Xls(Formatter):
    available = xlwt is not None

    def __call__(self, ts, filename=None, title=None, raw=False, **kwargs):
        '''Dump the timeseries to an xls representation.
            This function requires the python xlwt__ package.

        __ http://pypi.python.org/pypi/xlwt
        '''
        if isinstance(filename, xlwt.Workbook):
            wb = filename
        else:
            wb = xlwt.Workbook()
        title = title or ts.name
        sheet = wb.add_sheet(title)
        for i, row in enumerate(tsiterator(ts)):
            for j, col in enumerate(row):
                sheet.write(i, j, str(col))

        if raw:
            return wb
        else:
            stream = StringIO()
            wb.save(stream)
            return stream.getvalue()
