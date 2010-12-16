'''Rolling mean function for a numpy backend using pure python implementation'''
from _base import *

ts = randomts(100000, backend = 'numpy')

def run():
    cProfile.runctx("ts.rollmean(window=100, fallback = True)",
                    globals(),
                    locals(),
                    "Profile.prof")