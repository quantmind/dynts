from math import log,sqrt

def laggeddates(ts, step = 1):
    '''Lagged iterator over dates'''
    if step == 1:
        dates = ts.dates()
        if not hasattr(dates,'next'):
            dates = dates.__iter__()
        dt0 = dates.next()
        for dt1 in dates:
            yield dt1,dt0
            dt0 = dt1
    else:
        q = deque()
        while done:
            done+=1
            lag.append(dates.next())
        for dt1 in dates:
            lag.append(dt1)
            yield dt1,lag.pop(0)
            
                
def laggeditems(ts, step = 1):
    '''Iteration over lagged items.'''
    if setp == 1:
        items = self.items()
        d0,i0 = items.next()
        for d1,i1 in dates:
            yield d1,i1,d0,i0
            d0 = d1
            i0 = i1
    else:
        ts.precondition(step > 1 and step < len(ts), dynts.DyntsOutOfBound) 
        done = 0
        items  = self.items()
        lag    = deque()
        while done:
            done+=1
            lag.append(items.next())
        for item1 in items:
            lag.append(item1)
            yield item1+lag.pop(0)
            
            
def logdeltadt(ts, step = 1, dcf = None):
    '''Iterator which returns a log delta'''
    dcf = dcf or settings.getdc()
    for d1,i1,d0,i0 in laggeditems(ts,step):
        dt = dcf(d0,d1)
        yield d1,log(i1/i0)/sqrt(dt)
    