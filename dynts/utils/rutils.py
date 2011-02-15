# COLLECTIONS OF UTILITIES FOR USING R WITHIN PYTHON
#
#
from datetime import date, datetime, timedelta

from rpy2 import rinterface
from rpy2.robjects import r,numpy2ri

from dynts.exceptions import MissingPackage

def loadlib(lib):
    try:
        r('library(%s)' % lib)
    except rinterface.RRuntimeError:
        raise MissingPackage('R library %s not installed. From R shell type\n\ninstall.packages("%s")' % (lib,lib))

class rpyobject(object):
    _robj = None
    libraries = []
    scripts = []
    
    def __new__(cls, *args, **kwargs):
        obj = super(rpyobject,cls).__new__(cls)
        obj.r = cls.load()
        return obj
    
    @classmethod
    def load(cls):
        if not cls._robj:
            cls._robj = r
            for lib in cls.libraries:
                loadlib(lib)
            for script in cls.scripts:
                r(script)
            
        return cls._robj
    

# Convert to and From R date and python date
EPOCH = 1970
_EPOCH_ORD = date(EPOCH, 1, 1).toordinal()


def rdate0(dte):
    year, month, day = dte.timetuple()[:3]
    return date(year, month, 1).toordinal() - _EPOCH_ORD + day - 1

def rdate1(dte):
    year, month, day, hour, minute, second = dte.timetuple()[:6]
    days = date(year, month, 1).toordinal() - _EPOCH_ORD + day - 1
    return days + (hour + (minute + (second + 0.000001*dte.microsecond)/60.0)/60.0)/24.0

_converter = {datetime:rdate1,
              date:rdate0}

def py2rdate(dte):
    return _converter[dte.__class__](dte)


def r2pydate(tstamp):
    if not tstamp - round(tstamp):
        ordinal = _EPOCH_ORD + tstamp
        return date.fromordinal(ordinal)
    else:
        return datetime.fromordinal(tstamp)
    
    
def isoformat(dte):
    if isinstance(dte,datetime):
        raise NotImplementedError
    else:
        return dte.isoformat()
    