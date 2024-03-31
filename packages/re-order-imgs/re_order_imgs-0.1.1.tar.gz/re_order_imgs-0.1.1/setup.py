#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'exifread','Pillow']

test_requirements = ['pytest>=3', ]

setup(
    author="Mena Amin",
    author_email='info@synth9.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A py package for reordering images",
    entry_points={
        'console_scripts': [
            're_order_imgs=re_order_imgs.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='re_order_imgs',
    name='re_order_imgs',
    packages=find_packages(include=['re_order_imgs', 're_order_imgs.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/M-Farag/re_order_imgs',
    version='0.1.1',
    zip_safe=False,
)
