import os
import sys

def add2path(base, name):
    dir = os.path.join(base, name)
    if os.path.isdir(dir) and dir not in sys.path:
        sys.path.append(dir)
        
try:
    import pulsar
except ImportError:
    p = os.path
    base = p.dirname(p.dirname(p.abspath(__file__)))
    add2path(base, 'pulsar')
    add2path(base, 'ccy')
    try:
        import pulsar
    except ImportError:
        pulsar = None