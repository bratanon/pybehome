from setuptools import setup, find_packages

setup(
    name='pybehome',
    version='0.0.1',
    description='A python wrapper around WeBeHome OPEN API.',
    author='Emil Stjerneman',
    license='MIT',
    url='https://github.com/bratanon/pybehome',
    platforms='any',
    py_modules=['pybehome'],
    keywords='smart home automation webehome',
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=['requests>=2.20.0'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pybehome = pybehome.__main__:main'
        ]
    }
)
