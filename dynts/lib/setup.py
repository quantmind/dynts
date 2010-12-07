#
# Required by Cython to build extensions
#from numpy.distutils.core import setup
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules  = Extension('cts', ['src/cts.pyx'],
                         include_dirs=[numpy.get_include()])

setup(name='dynts.lib.cts',
      description = 'Cython library for dynts',
      ext_modules = [ext_modules],
      cmdclass = {'build_ext' : build_ext}
      )
