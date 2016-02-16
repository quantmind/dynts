from dynts import timeseries, nan
from dynts.utils import test


class TestClean(test.TestCase):

    def testClean(self):
        ts1 = self.timeseries(date=[1, 2, 3, 4, 5, 6],
                              data=[nan, nan, 5, 6, nan, -1])
        ts2 = self.timeseries(date=[1, 2, 3, 4, 5, 6, 7],
                              data=[nan, -4, 5, 6, -1, nan, -5])
        ts = ts1.merge(ts2)
        self.assertEqual(ts.count(), 2)
        self.assertEqual(len(ts), 7)
        cts = ts.clean()
        self.assertEqual(len(cts), 4)
        return ts

    def testClean2(self):
        ts1 = self.timeseries(date=[1, 2], data=[2, -1])
        ts2 = self.timeseries(date=[1, 2], data=[-4, nan])
        ts = ts1.merge(ts2)
        self.assertEqual(ts.count(), 2)
        self.assertEqual(len(ts), 2)
        cts = ts.clean()
        self.assertEqual(len(cts), 2)
        return ts

    def testItems(self):
        ts = self.testClean()
        v = list(ts.items(start_value=0))
        self.assertTrue(v)


@test.skipUnless(test.haszoo(), 'Requires R zoo package')
class TestCleanZoo(TestClean):
    backend = 'zoo'
