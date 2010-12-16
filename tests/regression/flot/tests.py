import unittest

import dynts
from dynts.utils.anyjson import json


class TestFlot(unittest.TestCase):
    
    def testFlot1(self):
        ts = dynts.evaluate('YHOO,GOOG').dump('flot')
        dts = ts.todict()
        self.assertEqual(dts['type'],'multiplot')
        self.assertEqual(len(dts['plots']),1)
        plot = dts['plots'][0]
        self.assertEqual(plot['type'],'timeseries')
        self.assertEqual(len(plot['series']),2)
        data = json.dumps(dts)
        