from setuptools import setup, find_packages
import os
os.system('export PYTHONPATH=~/module')

def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='pytobase',
  version='0.0.1',
  author='Zailox',
  author_email='zailox@mail.ru',
  description='This module will help you encrypt a python file using base64 encoding',
  long_description=readme(),
  long_description_content_type='text/markdown',
#  url='',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
#  project_urls={
 #   'GitHub': 'ZailoxTT'
  #},
  python_requires='>=3.6'
)