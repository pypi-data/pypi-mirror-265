from setuptools import setup
from os.path import join, dirname, abspath

# single version
__version__ = 'UNDEFINED'
# version.py should contain just the one line: __version__ = 'X.Y.Z'
with open(join(dirname(__file__), 'dcmextras', 'version.py')) as f:
    exec(f.read())


def readme(fname):
    path = abspath(join(dirname(__file__), fname))
    with open(path, encoding='utf-8') as f:
        return f.read()


config = {
    'name': 'dcmextras',
    'description': 'Additional dicom tools for pydicom and Siemens',
    'long_description': readme('README.md'),
    'long_description_content_type': 'text/markdown',
    'author': 'Ronald Hartley-Davies',
    'author_email': 'R.Hartley-Davies@physics.org',
    'version': __version__,
    'license': 'MIT',
    'url': 'https://bitbucket.org/rtrhd/dcmextras',
    'download_url': 'https://bitbucket.org/rtrhd/dcmextras/downloads/',
    'packages': ['dcmextras'],
    'install_requires': [
        'numpy>=1.13',
        'pydicom>=2.0'
    ],
    'tests_require': 'nibabel',
    'extras_require': {
        'tests': ['nibabel']
    },
    'scripts': ['bin/dcm2js'],
    'entry_points': {
        'console_scripts': ['phoenix=dcmextras.siemensphoenix:main'],
    },
    'classifiers': [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
}

setup(**config)
