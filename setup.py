from distutils.core import setup


setup(
    name='django_wagtailmedium',
    version='0.1',
    author='Dominique PERETTI',
    author_email='dperetti@lachoseinteractive.net',
    package_dir={'': 'project'},
    packages=['wagtailmedium'],
    package_data={'wagtailmedium': ['static/wagtailmedium/*.*']},
    url='http://github.com/dperetti/Django-wagtailmedium',
    license='LICENSE.txt',
    description='Wagtailmedium is a Medium Editor integration for the Wagtail CMS.',
    long_description=open('README.txt').read(),
    install_requires=[
        'Django>=1.7',
    ],
)
