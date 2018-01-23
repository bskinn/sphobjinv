from setuptools import setup

from sphobjinv import __version__


def readme():
    with open('README.rst', 'r') as f:
        return f.read()


setup(
    name='sphobjinv',
    version=__version__,
    packages=['sphobjinv'],
    install_requires=['attrs>=17', 'fuzzywuzzy>=0.3', 'jsonschema>=2.0',
                      'certifi'],
    provides=['sphobjinv'],
    requires=['attrs (>=17.1)', 'certifi', 'fuzzywuzzy (>=0.3)',
              'jsonschema (>=2.0)'],
    url='https://www.github.com/bskinn/sphobjinv',
    license='MIT License',
    author='Brian Skinn',
    author_email='bskinn@alum.mit.edu',
    description='Sphinx Objects.inv Encoder/Decoder',
    long_description=readme(),
    classifiers=['License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Environment :: Console',
                 'Framework :: Sphinx',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities',
                 'Development Status :: 5 - Production/Stable'],
    entry_points={
        'console_scripts': [
            'sphobjinv = sphobjinv.cmdline:main'
                           ]
                  }
)
