'''Quantitative financial timeseries analysis'''

VERSION = (0, 4, 2)
 
def get_version():
    return '.'.join(map(str,VERSION))
 
__version__  = get_version()
__license__  = "BSD"
__author__   = "Luca Sbardella"
__contact__  = "luca@quantmind.com"
__homepage__ = "http://github.com/quantmind/dynts/"
CLASSIFIERS  = [
                'Development Status :: 4 - Beta',
                'Environment :: Plugins',
                'Intended Audience :: Developers',
                'Intended Audience :: Financial and Insurance Industry',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: JavaScript',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3.1',
                'Programming Language :: Python :: 3.2',
                'Topic :: Scientific/Engineering',
                'Topic :: Scientific/Engineering :: Mathematics',
                'Topic :: Office/Business :: Financial'
                ]


from functools import reduce

from dynts.exceptions import *
from .backends import *
from .dsl import parse, evaluate, merge, dslresult, function_registry, functions
from .maths import BasicStatistics, pivottable
from .data import providers
from dynts import formatters
Formatters['flot'] = formatters.ToFlot()
Formatters['jsonvba'] = formatters.ToJsonVba()
Formatters['csv']  = formatters.ToCsv()
Formatters['excel']  = formatters.ToExcel()
Formatters['xls']  = formatters.ToXls()
Formatters['plot'] = formatters.ToPlot()


def statistics(expression,
               start = None,
               end = None,
               functions = None,
               multivariate = False, **kwargs):
    tseries = evaluate(expression, start = start, end = end, **kwargs).ts()
    if not multivariate:
        return BasicStatistics(tseries, functions = functions)
    else:
        raise NotImplementedError
    

def tsname(*names):
    from dynts.conf import settings
    sp = settings.splittingnames
    return reduce(lambda x,y: '%s%s%s' % (x,sp,y), names)


def composename(name, *names, **kwargs):
    from dynts.conf import settings
    sp = settings.splittingnames
    kw = ','.join(('{0}={1}'.format(*v) for v in kwargs.items()))
    if kw:
        kw = ','+kw
    return sp.join(('{0}({1}{2})'.format(name,x,kw) for x in names))
    

def hasextensions():
    '''True if cython extensions are available'''
    from .lib import hasextensions
    return hasextensions


def function_title_and_body(name,with_body=True):
    '''Given a function *name* return a tuple containing
the function title and the restructured text used to
create the function ducumentation.'''
    link = '.. _functions-{0}:'.format(name)
    func = function_registry[name]
    if func.description:
        title = '{0} - {1}'.format(name,func.description)
    else:
        title = name
    if with_body:
        under = (2+len(title))*'='
        fdoc = func.__doc__
        if not fdoc:
            raise FunctionError('Function {0} has no documentation.'.format(name))
        body = '\n'.join((link,'',title,under,'',fdoc,'\n'))
        return (title,body)
    else:
        return title


def function_doc(name):
    '''Given a function *name* return the restructured text used to
create the function ducumentation.'''
    return function_title_and_body(name)[1]

        
def functions_docs():
    names = sorted(function_registry)
    return '\n'.join((function_doc(name) for name in names))


def dump_docs(filename = 'dyntslist.rst'):
    docs = functions_docs()
    f = open(filename,'w')
    f.write(docs)
    f.close()
    print(('Saved function documentations in {0}'.format(filename)))
        