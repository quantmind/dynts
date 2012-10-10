'''Timeseries numpy implementation (default)'''
import dynts
from . import tsinterface, tsop, tsdelta, tsscalar, stat


class TestNumpyTS(tsinterface.TestTS):
    backend = 'numpy'


class TestOpNumpyTS(tsop.TestOperators):
    backend = 'numpy'
    

class TestDeltaNumpy(tsdelta.TestCase):
    backend = 'numpy'


class TestDeltaNumpy(tsscalar.TestCase):
    backend = 'numpy'


class TestStatNumpy(stat.TestStat):
    backend = 'numpy'


class TestDateNumpy(tsinterface.TestDates):
    backend = 'numpy'


if dynts.hasextensions():    
    class TestFallBackNumpyTS(tsinterface.TestFunctionTS):
        backend = 'numpy'
        fallback = True