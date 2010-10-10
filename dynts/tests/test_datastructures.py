import unittest
from itertools import izip

import dynts
from dynts.utils import skiplist, rollingOperation
from dynts.utils.populate import populate

class RollingFunctionSkipList(unittest.TestCase):
    
    def testSkipList(self):
        data  = populate(size = 500)[:,0]
        ol = skiplist(data = data)
        reduce(lambda x,y: self.assertTrue(y>x),ol)
        
    def testRollingOp(self):
        data  = populate(size = 500)[:,0]
        roll  = rollingOperation(data,20)
        rmin  = roll.min()
        rmax  = roll.max()
        rmed  = roll.median()
        for m0,m1,m2 in izip(rmin,rmed,rmax):
            self.assertTrue(m1>=m0)
            self.assertTrue(m2>=m1)
        
        