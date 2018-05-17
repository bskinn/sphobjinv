from setuptools import setup

from sphobjinv import __version__


def readme():
    with open('README.rst', 'r') as f:
        return f.read()


setup(
    name='sphobjinv',
    version=__version__,
    description='Sphinx Objects.inv Encoder/Decoder',
    long_description=readme(),
    url='https://github.com/bskinn/sphobjinv',
    license='MIT License',
    author='Brian Skinn',
    author_email='bskinn@alum.mit.edu',
    packages=['sphobjinv'],
    provides=['sphobjinv'],
    python_requires='>=3.4',
    requires=['attrs (>=17.1)', 'certifi', 'fuzzywuzzy (>=0.3)',
              'jsonschema (>=2.0)'],
    install_requires=['attrs>=17.1', 'certifi', 'fuzzywuzzy>=0.3',
                      'jsonschema>=2.0'],
    classifiers=['License :: OSI Approved',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Environment :: Console',
                 'Framework :: Sphinx',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Utilities',
                 'Development Status :: 5 - Production/Stable'],
    entry_points={
        'console_scripts': [
            'sphobjinv = sphobjinv.cmdline:main'
                           ]
                  }
)
