from setuptools import setup, find_packages

setup(
  name='private_rpa', 
  version='0.1.2',
  packages=find_packages(include=['private_rpa', 'private_rpa.*']),
  description='A custom private_rpa library with common utilities and cloud functionalities.',
  author='Prakash',
  license='MIT',
  install_requires=[],
)
