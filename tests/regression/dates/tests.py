from datetime import datetime

from dynts.test import TestCase
from dynts.lib.fallback import jstimestamp

class TestPythonDates(TestCase):
    
    def testTimeStamp(self):
        dt = datetime.now()
        ts = jstimestamp(dt)

