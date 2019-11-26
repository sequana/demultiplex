# -*- coding: utf-8 -*-
# License: 3-clause BSD
__revision__ = "$Id: $" # for the SVN Id
from setuptools import setup, find_namespace_packages

_MAJOR               = 0
_MINOR               = 8
_MICRO               = 0
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("yourname", "email@whatever.org")},
    'version': version,
    'license' : 'new BSD',
    'download_url' : ['http://pypi.python.org/pypi/sequana'],
    'url' : ["http://github.com/sequana/"],
    'description': "Pipeline that runs bcl2fastq and creates additional plots within a Snakemake workflow" ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['bcl2fastq, Illumina, bcl, fastq, demultiplexing, base caller'],
    'classifiers' : [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }


setup(
    name             = "sequana_demultiplex",
    version          = version,
    maintainer       = metainfo['authors']['main'][0],
    maintainer_email = metainfo['authors']['main'][1],
    author           = metainfo['authors']['main'][0],
    author_email     = metainfo['authors']['main'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    download_url     = metainfo['download_url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    packages = ["sequana_pipelines.demultiplex",
        'sequana_pipelines.demultiplex.data' ],

    install_requires = "sequana",

    # This is recursive include of data files
    exclude_package_data = {"": ["__pycache__"]},
    package_data = {
        '': ['config.yaml', "*.rules"],
        'sequana_pipelines.demultiplex.data' : ['*.*'], 
        },

    zip_safe=False,

    entry_points = {'console_scripts':[
        'sequana_pipelines_demultiplex=sequana_pipelines.demultiplex.main:main']
    }

)
