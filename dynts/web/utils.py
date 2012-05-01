from djpcms.html import table_header
from djpcms.utils.text import nicename


def data_table_header(splitter, base, *names, **params):
    '''Just a shortcut for adding live_data to the code'''
    code = splitter.join((n for n in names if n is not None)).lower()
    fullcode = splitter.join((base,code)).lower() if base else code
    name = params.pop('name',None) or nicename(code)
    return table_header(code, name, function=fullcode,
                        attrname=fullcode, **params)


class RollingStatistic(object):
    '''Utility for creating a statistic function headers to be used
in a table.'''
    splitter = '__'
    
    def __init__(self, code, name, description, function,
                 refresh, extraclass = 'color', base_code = None,
                 splitter = None):
        self.base_code = base_code
        self.code = code
        self.name = name
        self.description = description
        self.function = function
        self.refresh = refresh
        self.extraclass = extraclass
        self.splitter = splitter or self.splitter
        
    def __repr__(self):
        return self.code
    __str__ = __repr__
    
    def make_header(self, field = None, window = None):
        name = self.name(window)
        if field:
            name = '{0} {1}'.format(field,name)
        description = '' if not self.description else self.description(window)
        return data_table_header(self.splitter, self.base_code,
                                 field, window, self.code,
                                 name = name,
                                 description = description,
                                 extraclass = self.extraclass)