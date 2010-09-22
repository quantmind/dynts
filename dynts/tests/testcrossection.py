import unittest
from dynts.cross import section


class CrossectionTest(unittest.TestCase):
    
    def testAllGE(self):
        self.assertTrue(section([1,2]).allge([-1,1]))
        self.assertTrue(section([1,2,78]).allge([-1,1,56]))
        self.assertTrue(section([1,2,56]).allge([-1,1,56]))
        self.assertFalse(section([1,2,-5]).allge([-1,1,56]))
        
    def testAllLE(self):
        self.assertFalse(section([1,2]).allle([-1,1]))
        self.assertFalse(section([1,2,78]).allle([-1,1,56]))
        self.assertFalse(section([1,2,56]).allle([-1,1,56]))
        self.assertTrue(section([1,2,-5]).allle([4,2,56]))
        self.assertTrue(section([-90,1,-5]).allle([-1,1,56]))
    