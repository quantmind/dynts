'''Rolling min function for a numpy backend using pure python implementation'''
from _base import *

ts = randomts(10000, backend = 'numpy')

def run():
    cProfile.runctx("ts.rollmin(window=100, fallback = True)",
                    globals(),
                    locals(),
                    "Profile.prof")