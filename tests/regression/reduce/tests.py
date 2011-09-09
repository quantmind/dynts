import dynts
from dynts import test
from dynts.conf import settings
from dynts.test import TestCase
from dynts.utils.populate import randomts


class TestReduceAlgorithms(TestCase):
    
    def testsimple(self):
        ts = self.getts(size = 1000)
        rts = ts.reduce(size = 30)
        self.assertTrue(len(rts) <= 30)
        self.assertEqual(rts.end(),ts.end())
        
    
    