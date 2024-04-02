"""
The setup.py file for PyNUTClient
"""
# Based on https://medium.com/@VersuS_/automate-pypi-releases-with-github-actions-4c5a9cfe947d
# See also .github/workflows/PyNUTClient.yml for active packaging steps

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# README.txt appears from README.adoc during package or CI build
with codecs.open(os.path.join(here, "README.txt"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name =	"PyNUTClient",
    version =	'2.8.2',
    author =	"The Network UPS Tools project",
    license_files =	('LICENSE-GPL3',),
    author_email =	"jimklimov+nut@gmail.com",
    description =	"Python client bindings for NUT",
    url =	"https://github.com/networkupstools/nut/tree/master/scripts/python/module",
    long_description_content_type =	"text/plain",	# NOTE: No asciidoc so far, see https://packaging.python.org/en/latest/specifications/core-metadata/
    long_description =	long_description,
    packages   =	find_packages(),
    #py_modules =	['PyNUT'],
    package_dir =	{'PyNUT': 'PyNUTClient'},
    #data_files =	[('', ['tox.ini'])],
    #scripts    =	['PyNUTClient/test_nutclient.py', 'PyNUTClient/__init__.py'],
    python_requires =	'>=2.6',
    # install_requires =	['telnetlib'],	# NOTE: telnetlib.py is part of Python core for tested 2.x and 3.x versions, not something 'pip' can download
    keywords =	['pypi', 'cicd', 'python', 'nut', 'Network UPS Tools'],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)

