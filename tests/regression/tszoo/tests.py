'''Timeseries Zoo R package implementation'''
from regression import tsinterface, tsop, tsdelta, tsscalar, stat


class TestZooTS(tsinterface.TestTS):
    backend = 'zoo'


class TestOpNumpyTS(tsop.TestOperators):
    backend = 'zoo'
    

class TestDeltaZoo(tsdelta.TestCase):
    backend = 'zoo'
    

class TestScalarZoo(tsscalar.TestCase):
    backend = 'zoo'
    
    
class TestStatZoo(stat.TestStat):
    backend = 'zoo'