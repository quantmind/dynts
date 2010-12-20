from datetime import date, datetime


_EPOCH_ORD = 719163


def jstimestamp_slow(dte):
    '''Convert a date or datetime object into a javsacript timestamp'''
    year, month, day, hour, minute, second = dte.timetuple()[:6]
    days = date(year, month, 1).toordinal() - _EPOCH_ORD + day - 1
    hours = days*24 + hour
    minutes = hours*60 + minute
    seconds = minutes*60 + second
    if isinstance(dte,datetime):
        return 1000*seconds + 0.001*dte.microsecond
    else:
        return 1000*seconds


# 30% faster than jstimestamp_slow (no call to timetuple)
def jstimestamp(dte):
    '''Convert a date or datetime object into a javsacript timestamp.'''
    days = date(dte.year, dte.month, 1).toordinal() - _EPOCH_ORD + dte.day - 1
    hours = days*24
    
    if isinstance(dte,datetime):
        hours += dte.hour
        minutes = hours*60 + dte.minute
        seconds = minutes*60 + dte.second
        return 1000*seconds + int(0.001*dte.microsecond)
    else:
        return 3600000*hours

