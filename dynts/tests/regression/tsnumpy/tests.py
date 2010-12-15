'''Timeseries Numpy implementation'''
import dynts
from regression import tsinterface, tsop


class TestNumpyTS(tsinterface.TestTS):
    backend = 'numpy'


class TestOpNumpyTS(tsop.TestOperators):
    backend = 'numpy'


if dynts.hasextensions():
    
    class TestFallBackNumpyTS(tsinterface.TestFunctionTS):
        backend = 'numpy'
        fallback = True
    
    