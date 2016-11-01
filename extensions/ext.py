import os
from distutils.extension import Extension


path = os.path.join('extensions', 'lib')
ext_file = os.path.join(path, 'lib.c')


def params():
    cython = not os.path.isfile(ext_file)
    file_name = 'cts.pyx' if cython else 'cts.c'

    extension = Extension('pulsar.utils.lib',
                          [os.path.join(path, file_name)],
                          include_dirs=[path])

    extensions = [extension]

    return {'ext_modules': extensions,
            'include_dirs': [path]}
