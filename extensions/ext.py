import os
from distutils.extension import Extension
import pkg_resources


path = os.path.join('extensions', 'lib')
ext_file = os.path.join(path, 'lib.c')


def params():
    cython = not os.path.isfile(ext_file)
    file_name = 'cts.pyx' if cython else 'cts.c'
    numpy_incl = pkg_resources.resource_filename('numpy', 'core/include')

    extension = Extension('dynts.lib.cts',
                          [os.path.join(path, file_name)],
                          include_dirs=[numpy_incl, path])

    extensions = [extension]

    return {'ext_modules': extensions,
            'include_dirs': [path]}
