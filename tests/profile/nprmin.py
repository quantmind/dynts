'''Rolling min function for a numpy backend'''
from _base import *

ts = randomts(10000, backend = 'numpy')

def run():
    cProfile.runctx("ts.rollmin(window=100)",
                    globals(),
                    locals(),
                    "Profile.prof")
