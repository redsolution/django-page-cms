# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name='redsolutioncms.django-page-cms',
    version=__import__('pages').__version__,
    description=read('DESCRIPTION'),
    author='Batiste Bieler',
    author_email='batiste.bieler@gmail.com',
    url='http://code.google.com/p/django-page-cms/',
    download_url='http://code.google.com/p/django-page-cms/downloads/list',
    install_requires=(
        'html5lib>=0.10',
        'django-tagging>0.2.1',
        'django-mptt>=0.4.1',
        'BeautifulSoup',
        'django-authority==0.4',
    ),
    packages=find_packages(exclude=['example', 'example.*']),
    include_package_data=True, # include package data under svn source control
    long_description=read('README'),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    entry_points={
        'redsolutioncms': ['pages = pages.redsolution_setup', ],
    }
)
