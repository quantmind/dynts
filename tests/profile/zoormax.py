'''Rolling max function for a zoo backend'''
from _base import *

ts = randomts(10000, backend = 'zoo')


def run():
    cProfile.runctx("ts.rollmax(window=100)",
                    globals(),
                    locals(),
                    "Profile.prof")