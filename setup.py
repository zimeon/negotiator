"""Setup for negotiator2."""
from setuptools import setup
import re

# Extract version number from code. Be very strict about the
# format of the version string as a extra sanity check.
VERSIONFILE = "negotiator2/negotiator.py"
verfilestr = open(VERSIONFILE, "rt").read()
match = re.search(r"^__version__ = '(\d\.\d.\d+(\.\d+)?)'",
                  verfilestr, re.MULTILINE)
if match:
    version = match.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

setup(
    name='negotiator2',
    version=version,
    packages=['negotiator2'],
    install_requires=[],
    url='',
    author='Richard Jones and Simeon Warner',
    author_email='simeon.warner@cornell.edu',
    description="""
    Content Negotiation for Python

    The Negotiator is a library for decision making over Content Negotiation requests.
    It takes the standard HTTP Accept headers (Accept, Accept-Language, Accept-Charset,
    Accept-Encoding) and rationalises them against the parameters acceptable by the
    server; it then makes a recommendation as to the appropriate response format.

    This version of the Negotiator also supports the SWORDv2 extensions to HTTP Accept
    in the form of Accept-Packaging.
    """,
    license='CC0',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
