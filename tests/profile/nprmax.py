'''Rolling max function for a numpy backend'''
from _base import *

ts = randomts(10000, backend = 'numpy')

def run():
    cProfile.runctx("ts.rollmax(window=100)",
                    globals(),
                    locals(),
                    "Profile.prof")