from setuptools import setup, find_packages

setup(name='awap2019',
      version='2.0',
      description='Module for AWAP 2019.',
      long_description='Contains essential classes for competitors.',
      url='http://github.com/cuebeomc/awap2019',
      author='ACM@CMU',
      author_email='cuebeomc@andrew.cmu.edu',
      license='GPL',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'absl-py',
          'matplotlib',
          'scipy'
      ],
      )
