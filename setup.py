import os
from setuptools import find_packages, setup

from assetfiles import __version__

root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.md'), 'r') as file:
    README = file.read()

setup(
    name='django-assetfiles',
    version=__version__,
    description='Drop-in replacement for staticfiles which handles asset processing.',
    long_description=README,
    author='LocalMed',
    url='http://github.com/LocalMed/django-assetfiles',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
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
