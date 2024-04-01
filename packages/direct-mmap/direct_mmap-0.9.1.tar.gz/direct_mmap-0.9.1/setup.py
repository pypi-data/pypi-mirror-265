from setuptools import setup
import sys
import platform

if not sys.platform.startswith('linux'):
    raise Exception("This package can only be installed on Linux x86_64 systems.")

if platform.machine() != 'x86_64':
    raise Exception("This package can only be installed on Linux x86_64 systems.")

setup(
    name='direct_mmap',
    version='0.9.1',
    packages=['direct_mmap'],
    package_data={
        'direct_mmap': ['cpp/*.so', 'cpp/*.pyi', 'cpp/*.cpp', 'cpp/Makefile', 'Makefile']
    },
    python_requires='>=3.9',
    platforms=["manylinux2014_x86_64"]
)

