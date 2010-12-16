import time
from datetime import date, datetime
import json
    
date2timestamp = lambda dte : int(time.mktime(dte.timetuple()))
    
class JSONRPCEncoder(json.JSONEncoder):
    """
    Provide custom serializers for JSON-RPC.
    """
    def default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return date2timestamp(obj)
        else:
            raise exceptions.JSONEncodeException("%r is not JSON serializable" % (obj,))
        

class jsonPickler(object):
    
    def dumps(self, obj, **kwargs):
        return json.dumps(res, cls=JSONRPCEncoder, **kwargs)
    
    def loads(self,sobj):
        return json.loads(sobj)


class JSONobject(object):
    pickler = jsonPickler()
    
    def todict(self):
        d = self.__dict__.copy()
        d.pop('pickler',None)
        return d
    
    def tojson(self):
        return self.pickler.dumps(self.todict())
    
    
class JSONdatainfo(JSONobject):
    
    def __init__(self, data = None, info = None):
        self.data = data
        self.info = info
        
