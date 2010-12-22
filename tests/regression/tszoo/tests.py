'''Timeseries Zoo R package implementation'''
from regression import tsinterface, tsop, tsdelta, tsscalar


class TestNumpyTS(tsinterface.TestTS):
    backend = 'zoo'


class TestOpNumpyTS(tsop.TestOperators):
    backend = 'zoo'
    

class TestDeltaZoo(tsdelta.TestCase):
    backend = 'zoo'
    

class TestScalarZoo(tsscalar.TestCase):
    backend = 'zoo'