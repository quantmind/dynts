from datetime import datetime, date

from dynts.utils.anyjson import JSONdatainfo, JSONobject

EPOCH = 1970
_EPOCH_ORD = date(EPOCH, 1, 1).toordinal()


class MultiPlot(JSONdatainfo):
    '''Class holding several :class:`dynts.web.flot.Flot` instances.
    
    .. attribute:: plots
    
        list of :class:`dynts.web.flot.Flot` instances.
        
    .. attribute:: info
    
        Additional serialisable data
    '''
    def __init__(self, flot = None, info = None):
        super(MultiPlot,self).__init__(data = [], info = info)
        self.add(flot)
        
    def add(self, flot):
        '''Add a new :class:`dynts.web.flot.Flot` instance to :attr:`dynts.web.flot.MultiPlot.plots`.'''
        if isinstance(flot,Flot):
            self.data.append(flot)
        
    def todict(self):
        return {'type': 'multiplot',
                'info': self.info,
                'plots': [plot.todict() for plot in self.data]}
    

class Flot(JSONobject):
    '''A single plot which can be a timeseries or a XY plot.'''
    allowed_types = ['xy','timeseries']
    def __init__(self, name = '', type = None, shadowSize = None, **kwargs):
        if type not in self.allowed_types:
            type = 'xy'
        self.name   = name
        self.type   = type
        self.series = []
        df = {}
        self.options = df
        if shadowSize:
            df['shadowSize'] = shadowSize
        
    def add(self, serie):
        if isinstance(serie,Serie):
            self.series.append(serie)
        
    def todict(self):
        od = super(Flot,self).todict()
        od['series'] = [serie.todict() for serie in self.series]
        return od


class Serie(JSONobject):
    
    def __init__(self, label = '', data = None,
                 color = None, line = None, point = None,
                 shadowSize = None, yaxis = 1, xaxis = 1,
                 **kwargs):
        self.label = label
        if data is None:
            data = []
        self.data = data
        for k,v in kwargs.items():
            setattr(self,k,v)
        if isinstance(color,basestring):
            if not color.startswith('#'):
                color = '#%s' % color
        self.xaxis = xaxis
        self.yaxis = yaxis
        if color:
            self.color = color
        if isinstance(line,dict):
            self.lines = line
        if isinstance(line,dict):
            self.points = point
        if shadowSize:
            self.shadowSize = shadowSize


def pydate2flot(dte):
    year, month, day, hour, minute, second = dte.timetuple()[:6]
    days = date(year, month, 1).toordinal() - _EPOCH_ORD + day - 1
    hours = days*24 + hour
    minutes = hours*60 + minute
    seconds = minutes*60 + second
    if isinstance(dte,datetime):
        return 1000*seconds + 0.001*dte.microsecond
    else:
        return 1000*seconds

