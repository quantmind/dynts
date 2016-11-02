from dynts.utils import test


class TestReduceAlgorithms(test.TestCase):

    def test_simple(self):
        ts = self.getts(size = 1000)
        rts = ts.reduce(size = 30)
        self.assertTrue(len(rts) <= 30)
        self.assertEqual(rts.end(),ts.end())
