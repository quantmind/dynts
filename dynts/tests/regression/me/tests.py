import unittest

import dynts


class TestInitFile(unittest.TestCase):

    def test_version(self):
        self.assertTrue(dynts.VERSION)
        self.assertTrue(dynts.__version__)
        self.assertEqual(dynts.__version__,dynts.get_version())
        self.assertTrue(len(dynts.VERSION) >= 2)

    def test_meta(self):
        for m in ("__author__", "__contact__", "__homepage__", "__doc__"):
            self.assertTrue(getattr(dynts, m, None))