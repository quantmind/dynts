benchmarks = []
import timeit
#import cProfile as profiler


def run_timer(name, number, repeat, timer):
    v = min(timer.repeat(repeat=repeat,number=number))/number
    print('%s = %s' % (name,v))


test_maker = lambda name,timer : lambda number,repeat : run_timer(name, number, repeat, timer)


#def profile(name):
#    profiler.run("from unuk.http import tests\ntests.testers[%s]('%s')" % (n,url))



def makebench(name, **kwargs):
    '''Create a benchmark and added it to the list of benchmarks.'''
    global benchmarks
    timer = timeit.Timer(**kwargs)
    benchmarks.append(test_maker(name,timer))
    
    
    
def runbench(number = 5, repeat = 5):
    global benchmarks
    for b in benchmarks:
        b(number,repeat)
        