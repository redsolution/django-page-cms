# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='redsolutioncms.django-page-cms',
    test_suite="example.test_runner.run_tests",
    version=__import__('pages').__version__,
    description='A tree based Django CMS application, integrated with RedsolutionCMS',
    author='Batiste Bieler',
    author_email='batiste.bieler@gmail.com',
    url='http://code.google.com/p/django-page-cms/',
    download_url='http://code.google.com/p/django-page-cms/downloads/list',
    install_requires=(
        'html5lib>=0.10',
        'django-tagging>0.2.1',
        'django-mptt-2>0.2.1',
    ),
    packages=find_packages(exclude=['example', 'example.*']),
    include_package_data=True, # include package data under svn source control
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
        'grandma_setup': ['pages = pages.grandma_setup', ],
    }
)
