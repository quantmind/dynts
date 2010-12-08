from baseprofile import *

ts = randomts(10000, backend = 'numpy')

cProfile.runctx("ts.min()",
                globals(),
                locals(),
                "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()