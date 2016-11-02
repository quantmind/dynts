from ..conf import settings
from ..exc import FormattingException


class FormatterDict(dict):

    def oftype(self, typ):
        '''Return a generator of formatters codes of type typ'''
        for key, val in self.items():
            if val.type == typ:
                yield key


Formatters = FormatterDict()


class Data:
    '''Base class for data.

    An instance of this class contains a dataset of series.
    Each serie can be seen as an independent entity which, nevertheless,
    can have close tights with other series in the dataset.

    .. attribute:: name

        name of data object.

    .. attribute:: info

        additional information regarding data object.

    '''
    namespace = None

    def __init__(self, name, info):
        self.name = str(name or '')
        self.info = info

    def __repr__(self):
        d = self.description()
        b = '%s:%s' % (self.__class__.__name__ ,self.__class__.type)
        return '%s:%s' % (b, d) if d else b

    def __str__(self):
        return self.description()

    def description(self):
        return self.name

    def names(self, with_namespace=False):
        '''List of names for series in dataset.

        It will always return a list or names with length given by
        :class:`~.DynData.count`.
        '''
        N = self.count()
        names = self.name.split(settings.splittingnames)[:N]
        n = 0
        while len(names) < N:
            n += 1
            names.append('unnamed%s' % n)
        if with_namespace and self.namespace:
            n = self.namespace
            s = settings.field_separator
            return [n + s + f for f in names]
        else:
            return names

    def count(self):
        '''Number of series in dataset.'''
        raise NotImplementedError

    def series(self):
        '''Iterator over series in dataset.'''
        raise NotImplementedError

    def serie(self, index):
        '''Get serie data by column index.'''
        raise NotImplementedError

    def display(self):
        '''Nicely display self on the shell.

        Useful during prototyping and development.
        '''
        raise NotImplementedError

    def dump(self, format=None, **kwargs):
        """Dump the timeseries using a specific ``format``.
        """
        formatter = Formatters.get(format, None)
        if not format:
            return self.display()
        elif not formatter:
            raise FormattingException('Formatter %s not available' % format)
        else:
            return formatter(self, **kwargs)
