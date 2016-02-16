'''Rolling max function for a numpy backend'''
from datetime import datetime
from dynts.lib.fallback import jstimestamp


def timestamp():
    d = datetime.now()
    for i in range(10000):
        jstimestamp(d)


def run():
    cProfile.runctx("timestamp()",
                    globals(),
                    locals(),
                    "Profile.prof")
