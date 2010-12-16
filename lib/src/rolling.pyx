
#-------------------------------------------------------------------------------
# Rolling median, min, max

# Pointer to a function operating on a skiplist
ctypedef double_t (* skiplist_f)(skiplist sl, int n)

@cython.boundscheck(False)
cdef _roll_skiplist_op(ndarray arg, int window, skiplist_f op):
    '''Apply a rolling median/min/max function to an array'''
    cdef ndarray[double_t, ndim=1] input = arg
    cdef double val, prev, midpoint
    cdef skiplist sl
    cdef int nobs = 0
    cdef int i = 0
    cdef int j = 0
    cdef int N = len(input)
    
    if window > N:
        raise ValueError('Rolling operation not possible.')
    
    sl = skiplist(window)
    cdef ndarray[double_t, ndim=1] output = np.empty(N-window+1,
                                                     dtype=float)

    for i in xrange(window):
        val = input[i]
        # Not NaN
        if val == val:
            nobs += 1
            sl.insert(val)
    
    output[j] = op(sl, nobs)
    
    for i in xrange(window,N):
        val = input[i]
        prev = input[i - window]
        
        # Not NaN
        if prev == prev:
            sl.remove(prev)
            nobs -= 1
        # Not NaN
        if val == val:
            nobs += 1
            sl.insert(val)
        
        j += 1
        output[j] = op(sl, nobs)

    return output

def roll_median(ndarray input, int window):
    return _roll_skiplist_op(input, window, _get_median)

def roll_max(ndarray input, int window):
    return _roll_skiplist_op(input, window, _get_max)

def roll_min(ndarray input, int window):
    return _roll_skiplist_op(input, window, _get_min)


cdef double_t _get_median(skiplist sl, int nobs):
    cdef int midpoint
    if nobs:
        midpoint = nobs / 2
        if nobs % 2:
            return sl.get(midpoint)
        else:
            return (sl.get(midpoint) +
                    sl.get(midpoint - 1)) / 2
    else:
        return NaN


cdef double_t _get_max(skiplist sl, int nobs):
    if nobs:
        return sl.get(nobs - 1)
    else:
        return NaN


cdef double_t _get_min(skiplist sl, int nobs):
    if nobs:
        return sl.get(0)
    else:
        return NaN


#-------------------------------------------------------------------------------
# Rolling sum

@cython.boundscheck(False)
@cython.wraparound(False)
def roll_mean(ndarray[double_t, ndim=1] input, int window):
    '''Apply a rolling sum function to an array'''
    cdef double val, prev, sum_x = 0
    cdef int nobs = 0
    cdef int i = 0
    cdef int j = 0
    cdef int N = len(input)

    cdef ndarray[double_t, ndim=1] output = np.empty(N-window+1, dtype=float)

    for i in range(window):
        val = input[i]
        # Not NaN
        if val == val:
            nobs += 1
            sum_x += val
    
    output[j] = NaN if not nobs else sum_x / nobs

    for i in xrange(window,N):
        val = input[i]

        prev = input[j]
        if prev == prev:
            sum_x -= prev
            nobs -= 1

        if val == val:
            nobs += 1
            sum_x += val

        j += 1
        output[j] = NaN if not nobs else sum_x / nobs

    return output
