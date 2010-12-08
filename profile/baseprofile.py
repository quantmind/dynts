import os
try:
    import dynts
except ImportError:
    import sys
    p = lambda x : os.path.split(x)[0]
    path = p(p(os.path.abspath(__file__)))
    sys.path.insert(0, path)
    
import pstats, cProfile
from dynts.utils.populate import *