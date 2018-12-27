from setuptools import setup, find_packages

setup(name='awap2019',
      version='0.1.3',
      description='Module for AWAP 2019.',
      long_description='Contains essential classes for competitors.',
      url='http://github.com/cuebeomc/awap2019',
      author='ACM@CMU',
      author_email='cuebeomc@andrew.cmu.edu',
      license='GPL',
      packages=['awap2019'],
      install_requires=[
          'numpy',
      ],
      )
