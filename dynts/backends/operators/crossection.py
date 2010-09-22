from itertools import izip

crossoperator = lambda func,*args : [func(*vals) for vals in izip(*args)]

cmin = lambda *args : crossoperator(min,*args)
cmax = lambda *args : crossoperator(max,*args)
