from dynts.utils.py2py3 import zip

try:
    from .cts import *
    hasextensions = True
except ImportError as e:
    hasextensions = False
    from .fallback import *
else:
    import fallback

from .defaults import *

def makeskiplist(data = None, use_fallback = False):
    '''Create a new skiplist'''
    sl = fallback.skiplist if use_fallback else skiplist
    return sl(data)
