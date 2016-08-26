import os

from setuptools import setup

setup(
    name='assettomator',
    version='0.1.5',
    description='Asset Collector for Assetto Corsa Server Manager',
    url='https://github.com/PeteTheAutomator/ACServerManager',
    license='MIT',
    author='Peter Hehn',
    author_email='peter.hehn@yahoo.com',
    packages=[
        'acserver_libs',
    ],
    include_package_data=True,
    scripts=[
        'scripts/assetOmator.py',
    ],
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Systems Administrators',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[],
)
