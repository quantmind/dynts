'''Timeseries zoo/PerformanceAnalytics R package implementation'''
import sys
from unittest import skipUnless
from io import BytesIO

import dynts

from regression import tsinterface, tsop, tsdelta, tsscalar, stat

def haszoo():
    try:
        from dynts.backends.zoo import TimeSeries
    except ImportError:
        return False
    try:
        st = sys.stdout
        sys.stdout = BytesIO()
        t = TimeSeries()
        sys.stdout = st
        return True
    except dynts.MissingPackage:
        return False
    

@skipUnless(haszoo(),'rpy or zoo libraries not available')
class TestZooTS(tsinterface.TestTS):
    backend = 'zoo'


@skipUnless(haszoo(),'rpy or zoo libraries not available')
class TestOpNumpyTS(tsop.TestOperators):
    backend = 'zoo'
    

@skipUnless(haszoo(),'rpy or zoo libraries not available')
class TestDeltaZoo(tsdelta.TestCase):
    backend = 'zoo'
    

@skipUnless(haszoo(),'rpy or zoo libraries not available')
class TestScalarZoo(tsscalar.TestCase):
    backend = 'zoo'
    
    
@skipUnless(haszoo(),'rpy or zoo libraries not available')
class TestStatZoo(stat.TestStat):
    backend = 'zoo'