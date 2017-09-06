# Reference: https://github.com/pypa/sampleproject/blob/master/setup.py
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django_wagtailmedium',
    version='0.2',

    description='Wagtailmedium is a Medium Editor integration for the Wagtail CMS.',
    long_description=long_description,
    url='http://github.com/dperetti/Django-wagtailmedium',
    author='Dominique PERETTI',
    author_email='dperetti@lachoseinteractive.net',
    package_dir={'': 'project'},
    packages=['wagtailmedium'],
    package_data={'wagtailmedium': ['static/wagtailmedium/*.*']},
    license='LICENSE.txt',
    install_requires=[
        'Django>=1.7',
    ],
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',

    ],    
)
