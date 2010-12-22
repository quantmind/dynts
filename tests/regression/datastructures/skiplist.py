import unittest

try:
    from itertools import izip as zip
except ImportError:
    pass

import dynts
from dynts import lib
from dynts.stats import rollingOperation
from dynts.utils.populate import populate


class RollingFunctionSkipList(unittest.TestCase):
    fallback = False
    
    def setUp(self):
        self.skiplist = lib.fallback.skiplist if self.fallback else lib.skiplist
        
    def testSkipList(self):
        data  = populate(size = 500)[:,0]
        ol = lib.makeskiplist(data = data, use_fallback = self.fallback)
        reduce(lambda x,y: self.assertTrue(y>x),ol)
        
    def testRollingOp(self):
        data  = populate(size = 500)[:,0]
        roll  = rollingOperation(data, 20, skiplist_class = self.skiplist)
        rmin  = roll.min()
        rmax  = roll.max()
        rmed  = roll.median()
        for m0,m1,m2 in zip(rmin,rmed,rmax):
            self.assertTrue(m1>=m0)
            self.assertTrue(m2>=m1)
        
        
if dynts.hasextensions():
    
    class FallbackRollingFunctionSkipList(RollingFunctionSkipList):
        fallback = True