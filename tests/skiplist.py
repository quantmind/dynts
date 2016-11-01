import unittest

import dynts
from dynts import lib
from dynts.stats import rollingOperation
from dynts.utils.populate import populate


class RollingFunctionSkipList(unittest.TestCase):
    fallback = False

    def setUp(self):
        self.skiplist = lib.fallback.skiplist if self.fallback else lib.skiplist

    def make(self):
        data  = populate(size = 500)[:,0]
        sl = lib.makeskiplist(data = data, use_fallback = self.fallback)
        self.assertEqual(len(sl),500)
        return sl

    def testSkipList(self):
        ol = self.make()
        p = None
        for v in ol:
            if p is not None:
                self.assertTrue(v>=p)
            p = v

    def testRank(self):
        sl = self.make()
        for i in range(len(sl)):
            self.assertEqual(sl.rank(sl[i]),i)
        self.assertRaises(IndexError, lambda : sl[10000])
        N = len(sl)
        v1 = sl[100]
        v0 = sl[99]
        r = sl.rank(0.5*(v1 + v0))
        self.assertEqual(r,-99)
        self.assertEqual(sl.rank(sl[0]-1),-1)
        self.assertEqual(sl.rank(sl[N-1]+1),-N+1)

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
