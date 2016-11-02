from .cts import *      # noqa
from . import defaults  # noqa
from . import fallback


def make_skiplist(data=None, use_fallback=False):
    '''Create a new skiplist'''
    sl = fallback.skiplist if use_fallback else skiplist
    return sl(data)
