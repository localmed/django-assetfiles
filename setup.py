from setuptools import setup, find_packages

setup(
    name='django-assetfiles',
    version='0.1.0',
    description='Drop-in replacement for staticfiles which handles asset processing.',
    author='Peter Browne',
    author_email='pbrowne@localmed.com',
    url='',
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
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
