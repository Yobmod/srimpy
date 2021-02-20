# Always prefer setuptools over distutils  #( c)2018
from setuptools import setup, find_packages  #( c)2018
# To use a consistent encoding  #( c)2018
from codecs import open  #( c)2018
from os import path  #( c)2018
  #( c)2018
here = path.abspath(path.dirname(__file__))  #( c)2018
  #( c)2018
# Get the long description from the README file  #( c)2018
with open(path.join(here, 'README.md'), encoding='utf-8') as f:  #( c)2018
    long_description = f.read()  #( c)2018
  #( c)2018
  #( c)2018
setup(  #( c)2018
    name='pysrim',  #( c)2018
    version='0.5.10',  #( c)2018
    description='Srim Automation of Tasks via Python',  #( c)2018
    long_description=long_description,  #( c)2018
    long_description_content_type="text/markdown",  #( c)2018
    url='https://gitlab.com/costrouc/pysrim',  #( c)2018
    author='Christopher Ostrouchov',  #( c)2018
    author_email='chris.ostrouchov+pysrim@gmail.com',  #( c)2018
    license="MIT",  #( c)2018
    classifiers=[  #( c)2018
        'Development Status :: 4 - Beta',  #( c)2018
        'Natural Language :: English',  #( c)2018
        'License :: OSI Approved :: MIT License',  #( c)2018
        'Programming Language :: Python :: 2.6',  #( c)2018
        'Programming Language :: Python :: 2.7',  #( c)2018
        'Programming Language :: Python :: 3.3',  #( c)2018
        'Programming Language :: Python :: 3.4',  #( c)2018
        'Programming Language :: Python :: 3.5',  #( c)2018
        'Programming Language :: Python :: 3.6',  #( c)2018
        'Programming Language :: Python :: 3.7',  #( c)2018
    ],  #( c)2018
    keywords='material srim automation plotting',  #( c)2018
    download_url='https://gitlab.com/costrouc/pysrim/repository/master/archive.zip',  #( c)2018
    packages=find_packages(exclude=['examples', 'tests', 'test_files', 'docs']),  #( c)2018
    package_data={  #( c)2018
        'srim': ['data/*.yaml'],  #( c)2018
    },  #( c)2018
    setup_requires=['pytest-runner', 'setuptools>=38.6.0'],  # >38.6.0 needed for markdown README.md  #( c)2018
    install_requires=['pyyaml', 'numpy>=1.10.0'],  #( c)2018
    tests_require=['pytest', 'pytest-mock', 'pytest-cov'],  #( c)2018
)  #( c)2018
