from setuptools import setup


def readme():
    with open('README.rst', 'r') as f:
        return f.read()


setup(
    name='sphobjinv',
    version='2.0.dev1',
    packages=['sphobjinv'],
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
