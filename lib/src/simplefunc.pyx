

def tsminmax(ndarray[double_t, ndim=1] input):
    cdef double mv, xv = 0
    cdef int N = len(input)
    if not N:
        return (NaN,NaN)
    
    mv = input[0]
    xv = input[0]
    for i in xrange(1,N):
        v = input[i]
        mv = min(mv,v)
        xv = max(xv,v)
    
    return (mv,xv)