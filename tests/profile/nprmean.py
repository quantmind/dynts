'''Rolling mean function for a numpy backend'''
from _base import *

ts = randomts(100000, backend = 'numpy')

def run():
    cProfile.runctx("ts.rollmean(window=100)",
                    globals(),
                    locals(),
                    "Profile.prof")