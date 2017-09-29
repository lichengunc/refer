# -*- coding: utf-8 -*-
"""Setup script for refer.

mask.so is compiled as a Cython extension used to visualize the segmentation
of referred object.
All "mask" related code is copied from https://github.com/pdollar/coco.git
"""

# Standard library imports
import os
import ast

# Third party imports
import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup


HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='referit'):
    """Get version from text file and avoids importing the module."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


ext_modules = [
    Extension(
        'referit.external._mask',
        sources=['referit/external/maskApi.c', 'referit/external/_mask.pyx'],
        include_dirs=[np.get_include(), 'external'],
        extra_compile_args=['-Wno-cpp', '-Wno-unused-function', '-std=c99'],
    )
]

REQUIREMENTS = ['cython', 'numpy', 'matplotlib', 'scikit-image']

setup(
    name='referit',
    version=get_version(),
    keywords=['referit', 'segmentation', 'dataset'],
    url='https://github.com/lichengunc/refer',
    license='MIT',
    author='Licheng Yu',
    author_email='licheng@cs.unc.edu',
    description='Python wrapper to load the ReferIt Game dataset',
    ext_modules=cythonize(ext_modules),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
