from setuptools import setup, find_packages  
from os import path
# from codecs import open
from pathlib import Path

import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='srimpy', 
    version='0.6.3',  
    description='Wrapper scripts for Srim analysis and multi-processing',
    long_description=README, 
    long_description_content_type="text/markdown", 
    url='https://gitlab.com/yobmod/srimpy',
    author='Dominic Laventine', 
    author_email='yobmod+srimpy@gmail.com',
    license="MIT", 
    classifiers=[ 
        'Development Status :: 4 - Beta',
        'Natural Language :: English', 
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3", 
        'Programming Language :: Python :: 3.6',  
        'Programming Language :: Python :: 3.7', 
        'Programming Language :: Python :: 3.8',  
        'Programming Language :: Python :: 3.9', 
        'Programming Language :: Python :: 3.10',  
    ],
    keywords='srim analysis ionization parallel processing plotting',
    download_url='https://github.com/Yobmod/srimpy/archive/main.zip',
    packages=find_packages(exclude=['examples', 'tests', 'test_files']),
    package_data={
        'srim': ['data/*.yaml', 'data/*.toml', 'data/*.json' ],
    },
    include_package_data=True,
    setup_requires=['pytest-runner', 'setuptools>=40.0.0'],  
    install_requires=['pyyaml', 'numpy>=1.15.0' 'matplotlib>=3.0.0'],
    tests_require=['pytest', 'pytest-mock', 'pytest-cov', 'pytest-srcpaths'],
)
