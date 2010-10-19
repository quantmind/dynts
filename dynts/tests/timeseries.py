from dynts.tests import tsinterface
from dynts.tests import testop

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
    