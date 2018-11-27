from setuptools import setup, find_packages

setup(
    name='pybehome',
    version='0.0.1',
    description='A python wrapper around WeBeHome OPEN API.',
    url='https://github.com/bratanon/pybehome',
    author='Emil Stjerneman',
    author_email='emil@stjerneman.com',
    license='MIT',
    install_requires=['requests>=2.20.0'],
    packages=find_packages(),
)