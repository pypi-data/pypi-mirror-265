#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jan Wrobel",
    author_email='jan@mixedbit.org',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
    description="Python virtual environment which jails executed programs.",
    entry_points={
        'console_scripts': [
            'venvjail=venvjail.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    # TODO: reenable
    # + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='venvjail',
    name='venvjail',
    packages=find_packages(include=['venvjail', 'venvjail.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/wrr/venvjail',
    version='0.0.0',
    zip_safe=False,
)
