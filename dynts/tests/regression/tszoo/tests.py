'''Timeseries Zoo R package implementation'''
from regression import tsinterface, tsop


class TestNumpyTS(tsinterface.TestTS):
    backend = 'zoo'


class TestOpNumpyTS(tsop.TestOperators):
    backend = 'zoo'
    