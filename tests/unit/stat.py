
from numpy import outer, cov, transpose, zeros

import dynts
from dynts.utils import test
from dynts.utils.populate import datepopulate, populate
from dynts.stats import Variates, vector_to_symmetric

places = 4


class TestStat(test.TestCase):

    def testVar(self):
        '''Calculate the biased variance of a series'''
        ts = dynts.timeseries(date=datepopulate(10), data=range(1, 11),
                              backend=self.backend)
        self.assertAlmostEqual(ts.var()[0], 8.25, places)
        self.assertAlmostEqual(ts.var(ddof=1)[0], 9.166667, places)

    def testVectorToSymmetric(self):
        self.assertRaises(ValueError, vector_to_symmetric, [1, 2])
        self.assertRaises(ValueError, vector_to_symmetric, [1, 2, 4, 6])
        c = vector_to_symmetric([4.5])
        self.assertEqual(c.shape, (1, 1))
        self.assertEqual(c[0, 0], 4.5)
        c = vector_to_symmetric([4.5, -7.1, 5])
        self.assertEqual(c.shape, (2, 2))
        self.assertEqual(c[0, 0], 4.5)
        self.assertEqual(c[1, 1], 5)
        self.assertEqual(c[0, 1], -7.1)
        self.assertEqual(c[1, 0], -7.1)

    def testVariate(self):
        N = 3
        data = populate(100, N)
        dsum = sum(data)
        dsum2 = zeros((N, N))
        for cross in data:
            dsum2 += outer(cross, cross)
        v = Variates(100, dsum, dsum2)
        self.assertAlmostEqual(cov(data, rowvar=0), v.cov(), places)
        self.assertAlmostEqual(cov(data, ddof=0, rowvar=0),
                               v.cov(ddof=0), places)


@test.skipUnless(test.haszoo(), 'Requires R zoo package')
class TestStatZoo(TestStat):
    backend = 'zoo'
