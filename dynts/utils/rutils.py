from datetime import date, datetime, timedelta
from dynts.exceptions import MissingPackage
from rpy2 import rinterface
from rpy2.robjects import r,numpy2ri

def loadlib(lib):
    try:
        r('library(%s)' % lib)
    except rinterface.RRuntimeError:
        raise MissingPackage('R library %s not installed. From R shell type\n\ninstall.packages("%s")' % (lib,lib))

class rpyobject(object):
    _robj = None
    libraries = []
    
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
                    
        return cls._robj
    

# Convert to and From R date and python date
rdate0 = date(1970,1,1)
py2rdate = lambda x : (x-rdate0).days
r2pydate = lambda x : rdate0 + timedelta(days = int(x))

def isoformat(dte):
    if isinstance(dte,datetime):
        raise NotImplementedError
    else:
        return dte.isoformat()
    