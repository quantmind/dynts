from regression.interface import tsinterface, testop


class TestZooTS(tsinterface.TestTS):
    backend = 'zoo'

class TestNumpyTS(tsinterface.TestTS):
    backend = 'numpy'


class TestOpZooTS(testop.TestOperators):
    backend = 'zoo'

class TestOpNumpyTS(testop.TestOperators):
    backend = 'numpy'


#class TestRmetricsTS(tsbase.TestTS):
#    backend = 'rmetrics'
    