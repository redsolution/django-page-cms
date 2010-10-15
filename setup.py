# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
package_name = 'django-page-cms'

def local_open(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

setup(
    name='redsolutioncms.django-page-cms',
    version=__import__('pages').__version__,
    description='A tree based Django CMS application, integrated with RedsolutionCMS',
    author='Batiste Bieler',
    author_email='batiste.bieler@gmail.com',
    url='http://code.google.com/p/django-page-cms/',
    download_url='http://code.google.com/p/django-page-cms/downloads/list',
    install_requires=(
        'html5lib>=0.10',
        'django-tagging>0.2.1',
        'django-mptt>=0.4.1',
        'BeautifulSoup',
    ),
    packages=find_packages(exclude=['example', 'example.*']),
    include_package_data=True, # include package data under svn source control
    long_description=local_open('README.rst').read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
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
