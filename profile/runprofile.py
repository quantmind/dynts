import os
import sys
import pstats, cProfile
from optparse import OptionParser


def makeoptions():
    parser = OptionParser()
    parser.add_option("-s", "--sort",
                      action="store",
                      dest="sort_stats",
                      default='time',
                      help="Profile sort method: time, file, cumulative")
    parser.add_option("-l", "--list",
                      action="store_true",
                      dest="show_list",
                      default=False,
                      help="Show the list of available profiling tests")
    return parser




def addpath():
    try:
        import dynts
    except ImportError:
        p = lambda x : os.path.split(x)[0]
        path = p(p(os.path.abspath(__file__)))
        sys.path.insert(0, path)
    


def get_tests():
    from dynts.utils import import_module
    p = os.path
    cur  = p.split(p.abspath(__file__))[0]
    if cur not in sys.path:
        sys.path.insert(0,cur)
    path = p.join(cur,'ptests')
    tests = {}
    for d in os.listdir(path):
        if d.startswith('_'):
            continue
        name = d.split('.')[0]
        mod  = import_module('ptests.{0}'.format(name))
        tests[name] = mod
    return tests
        


if __name__ == '__main__':
    addpath()
    options, tags = makeoptions().parse_args()
    ld = get_tests()
    if options.show_list:
        import dynts
        dynts.showtestlist(ld)
    else:
        if tags:
            name = tags[0]
            mod = ld.get(name,None)
            if mod:
                mod.run()
                s = pstats.Stats("Profile.prof")
                s.strip_dirs().sort_stats("time").print_stats()
            else:
                print('Unknonw test {0}.'.format(name))
        else:
            print('You need to pass a profile test name to profile.')
            print('Check the list by typing runprofile --list.')
            