from distutils.core import setup

setup(name='PyRSA',
    python_requires='>3',
    version='0.1',
    description='A simple implementation of PyCryptodome for RSA encryption in a CLI interface.',
    url='https://github.com/Nobody912/PyRSA',
    author='Erik Ji',
    author_email='erikji@tuta.io',
    license='MIT',
    packages=['pyrsa',],
    dependency_links=[
        'https://github.com/pwaller/pyfiglet/tarball/0.7.3'
    ],
    install_requires=[
        'termcolor',
        'pycryptodome',
    ],
    zip_safe=False)