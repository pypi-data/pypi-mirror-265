from distutils.core import setup
from setuptools import find_packages

from cval_lib.version import VERSION

setup(
    name='cval-lib',
    version=VERSION,
    description='python computer vision active learning library',
    author='DGQ | Cyrill Belyakov',
    author_email='',
    url='https://cval.ai',
    package_dir={
        '': '.',
    },
    packages=find_packages(include=['cval_lib', 'cval_lib.*']),
    install_requires=[
        'pydantic==1.10.9',
        'requests>=2.31.0',
        'loguru==0.7.0',
    ]
)
