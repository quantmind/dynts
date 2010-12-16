'''Rolling max function for a numpy backend'''
from _base import *

ts = randomts(10000, 5, backend = 'numpy')

def run():
    cProfile.runctx("ts.delta(lag=1)",
                    globals(),
                    locals(),
                    "Profile.prof")