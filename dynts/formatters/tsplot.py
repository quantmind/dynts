import matplotlib.pyplot as plt

def toplot(ts, filename = None, **kwargs):
    '''To plot formatter'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dates = list(ts.dates())
    ax.plot(dates, ts.values())
    #ax.xaxis.set_major_locator(years)
    #ax.xaxis.set_major_formatter(yearsFmt)
    #ax.xaxis.set_minor_locator(months)
    #datemin = datetime.date(r.date.min().year, 1, 1)
    #datemax = datetime.date(r.date.max().year+1, 1, 1)
    #ax.set_xlim(datemin, datemax)
    
    # format the coords message box
    #def price(x): return '$%1.2f'%x
    #ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    #ax.format_ydata = price
    ax.grid(True)
    
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    return plt
    