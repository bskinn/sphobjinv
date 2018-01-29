from setuptools import setup

from sphobjinv import __version__

setup(
    name='sphobjinv',
    version=__version__,
    packages=['sphobjinv'],
    provides=['sphobjinv'],
    url='https://www.github.com/bskinn/sphobjinv',
    license='MIT License',
    author='Brian Skinn',
    author_email='bskinn@alum.mit.edu',
    description='Sphinx Objects.inv Encoder/Decoder',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Environment :: Console',
                 'Framework :: Sphinx',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities',
                 'Development Status :: 5 - Production/Stable'],
    entry_points={
        'console_scripts': [
            'sphobjinv = sphobjinv.sphobjinv:main'
                           ]
                  }
)
