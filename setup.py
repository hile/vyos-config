
from setuptools import setup, find_packages
from vyos import __version__

setup(
    name='vyos-config',
    keywords='vyos configuration parser',
    description='Tool to parse VyOS configuration',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://github.com/hile/vyos-config',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vyos-config=vyos.bin.vyos_config:main',
        ],
    },
    install_requires=(
        'systematic>=4.8.4',
    ),
    setup_requires=['pytest-runner'],
    tests_require=(
        'pytest',
        'pytest-runner',
        'pytest-datafiles',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
