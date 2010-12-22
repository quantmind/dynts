'''Rolling max function for a numpy backend'''
from datetime import datetime
from _base import *
from dynts.lib.fallback import jstimestamp 


def timestamp():
    d = datetime.now()
    for i in xrange(10000):
        jstimestamp(d)

    
def run():
    cProfile.runctx("timestamp()",
                    globals(),
                    locals(),
                    "Profile.prof")