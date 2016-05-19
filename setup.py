from setuptools import setup

setup(
    name='sphobjinv',
    version='0.1',
    packages=['sphobjinv'],
#    package_data={'opan': ['test/resource/test.trj',
#                           'test/resource/inertia/*.hess',
#                           'test/resource/inertia/*.xyz',
#                           'test/resource/orca/test_orca*']},
    url='https://www.github.com/bskinn/sphobjinv',
    license='The MIT License',
    author='Brian Skinn',
    author_email='bskinn@alum.mit.edu',
    description='Intersphinx objects.inv Encoder/Decoder',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities',
                 'Development Status :: 4 - Beta'],
    entry_points={
        'console_scripts': [
            'sphobjinv = sphobjinv.sphobjinv:main'
                           ]
                  }
)
