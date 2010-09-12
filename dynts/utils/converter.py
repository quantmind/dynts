import time
from datetime import datetime, date, timedelta

def date2timestamp(dte):
    return time.mktime(dte.timetuple())


def timestamp2date(tstamp):
    "Converts a unix timestamp to a Python datetime object"
    return datetime.fromtimestamp(tstamp).date()


def posixtime(year = 2002, month = 1, day = 1):
    bd = boostdate(year,month,day)
    return bd.timegm() == calendar.timegm((year,month,day,0,0,0))