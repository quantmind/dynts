'''Rolling mean function for a zoo backend'''
from _base import *

ts = randomts(100000, backend = 'zoo')


def run():
    cProfile.runctx("ts.rollmean(window=100)",
                    globals(),
                    locals(),
                    "Profile.prof")
