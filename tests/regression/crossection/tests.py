import unittest
from dynts.utils import cross


class CrossectionTest(unittest.TestCase):
    
    def testAllGE(self):
        self.assertTrue(cross([1,2]) >= [-1,0.5])
        self.assertTrue(cross([1,2,78]) >= [-1,1,56])
        self.assertTrue(cross([1,2,56]) >= [-1,1,56])
        self.assertFalse(cross([1,2,-5]) >= [-1,1,56])
        
    def testAllLE(self):
        self.assertFalse(cross([1,2]) <= [-1,1])
        self.assertFalse(cross([1,2,78]) <= [-1,1,56])
        self.assertFalse(cross([1,2,56]) <= [-1,1,56])
        self.assertTrue(cross([1,2,-5]) <= [4,2,56])
        self.assertTrue(cross([-90,1,-5]) <= [-1,1,56])
    