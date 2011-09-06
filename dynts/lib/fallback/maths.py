

def bindata(data, maxbins = 30, reduction = 0.1):
    '''
data must be numeric list with a len above 20
This function counts the number of data points in a reduced array
'''
    tole = 0.01
    N = len(data)
    assert N > 20
    vmin = min(data)
    vmax = max(data)
    DV = vmax - vmin
    tol = tole*DV
    vmax += tol
    if vmin >= 0:
        vmin -= tol
        vmin = max(0.0,vmin)
    else:
        vmin -= tol
    n = min(maxbins,max(2,int(round(reduction*N))))
    DV = vmax - vmin
    bbin = npy.linspace(vmin,vmax,n+1)
    sso = npy.searchsorted(bbin,npy.sort(data))
    x = []
    y = []
    for i in range(0,n):
        x.append(0.5*(bbin[i+1]+bbin[i]))
        y.append(0.0)
    dy = 1.0/N
    for i in sso:
        y[i-1] += dy/(bbin[i]-bbin[i-1])
    return (x,y)