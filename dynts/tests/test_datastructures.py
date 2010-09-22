import unittest
from itertools import izip

import dynts
from dynts.utils.populate import populate
from dynts.utils.skiplist import RollingOrderedListOperation


class RollingFunctionSkipList(unittest.TestCase):
    
    def testRollingOp(self):
        data  = populate(size = 500)[:,0]
        roll  = RollingOrderedListOperation(data,20)
        rmin  = roll.min()
        rmax  = roll.max()
        rmed  = roll.median()
        for m0,m1,m2 in izip(rmin,rmed,rmax):
            self.assertTrue(m1>=m0)
            self.assertTrue(m2>=m1)
        
        