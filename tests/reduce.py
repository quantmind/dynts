import dynts
from dynts.utils import test
from dynts.utils.populate import randomts


class TestReduceAlgorithms(test.TestCase):
    
    def testsimple(self):
        ts = self.getts(size = 1000)
        rts = ts.reduce(size = 30)
        self.assertTrue(len(rts) <= 30)
        self.assertEqual(rts.end(),ts.end())
        
    
    