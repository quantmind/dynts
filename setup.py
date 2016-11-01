#!/usr/bin/env python
import sys
import os

from setuptools import setup, find_packages
from extensions import ext

import dynts


def read(name):
    filename = os.path.join(os.path.dirname(__file__), name)
    with open(filename) as fp:
        return fp.read()


def requirements(name):
    install_requires = []
    dependency_links = []

    for line in read(name).split('\n'):
        if line.startswith('-e '):
            link = line[3:].strip()
            if link == '.':
                continue
            dependency_links.append(link)
            line = link.split('=')[1]
        line = line.strip()
        if line:
            install_requires.append(line)

    return install_requires, dependency_links


meta = dict(
    version=dynts.__version__,
    description=dynts.__doc__,
    name='dynts',
    author="Luca Sbardella",
    author_email="luca@quantmind.com",
    maintainer_email="luca@quantmind.com",
    url="https://github.com/quantmind/dynts",
    license="BSD",
    long_description=read('README.rst'),
    include_package_data=True,
    setup_requires=['wheel'],
    packages=find_packages(include=['dynts', 'dynts.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Office/Business :: Financial'
    ]
)


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command == 'agile':
        from agile.app import AgileManager
        AgileManager(description='Release manager for dynts',
                     argv=sys.argv[2:]).start()
    else:
        meta.update(ext.params())
        setup(**meta)
