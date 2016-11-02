from datetime import datetime

from dynts.utils import test
from dynts.lib.fallback import jstimestamp


class TestPythonDates(test.TestCase):

    def testTimeStamp(self):
        dt = datetime.now()
        ts = jstimestamp(dt)

