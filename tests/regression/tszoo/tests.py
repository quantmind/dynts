'''Timeseries Zoo R package implementation'''
from regression import tsinterface, tsop, tsdelta


class TestNumpyTS(tsinterface.TestTS):
    backend = 'zoo'


class TestOpNumpyTS(tsop.TestOperators):
    backend = 'zoo'
    

class TestDeltaZoo(tsdelta.TestCase):
    backend = 'zoo'