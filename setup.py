import os
from setuptools import setup, find_packages

from assetfiles import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-assetfiles',
    version=__version__,
    description='Drop-in replacement for staticfiles which handles asset processing.',
    long_description=README,
    author='Peter Browne',
    author_email='pbrowne@localmed.com',
    url='http://github.com/LocalMed/django-assetfiles',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
