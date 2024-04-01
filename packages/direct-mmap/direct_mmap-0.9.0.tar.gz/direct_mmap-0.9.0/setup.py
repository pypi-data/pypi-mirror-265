from setuptools import setup

setup(
    name='direct_mmap',
    version='0.9.0',
    packages=['direct_mmap'],
    package_data={
        'direct_mmap': ['cpp/*.so', 'cpp/*.pyi', 'cpp/*.cpp', 'cpp/Makefile', 'Makefile']
    },
    python_requires='>=3.9',
    platforms=["manylinux2014_x86_64"]
)

