from setuptools import setup, find_packages  
from os import path
# from codecs import open
from pathlib import Path

# root = path.abspath(path.dirname(__file__)) 
root = Path(__file__).parent.absolute()

# Get description from the README file
with open(root / 'README.md', encoding='utf-8') as f:
    ld = f.read()

setup(
    name='srimpy', 
    version='0.6.0',  
    description='Wrapper scipts for Srim analysis',
    long_description=ld, 
    long_description_content_type="text/markdown", 
    url='https://gitlab.com/yobmod/srimpy',
    author='Dominic Laventine', 
    author_email='yobmod+srimpy@gmail.com',
    license="MIT", 
    classifiers=[ 
        'Development Status :: 4 - Beta',
        'Natural Language :: English', 
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3.6',  
        'Programming Language :: Python :: 3.7', 
        'Programming Language :: Python :: 3.8',  
        'Programming Language :: Python :: 3.9', 
        'Programming Language :: Python :: 3.10',  
    ],
    keywords='srim analysis ionization parallel processing plotting',
    download_url='https://github.com/Yobmod/srimpy/archive/main.zip',
    packages=find_packages(exclude=['examples', 'tests', 'test_files', 'docs']),  #( c)2018
    package_data={
        'srim': ['data/*.yaml'],  #( c)2018
    },
    setup_requires=['pytest-runner', 'setuptools>=40.0.0'],  
    install_requires=['pyyaml', 'numpy>=1.11.0'],
    tests_require=['pytest', 'pytest-mock', 'pytest-cov'],   #( c)2018
)
