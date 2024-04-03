#!/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2022--, Panpiper development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="panpiper",
    version="1.0.1",
    license='BSD-3-Clause',
    author="Renee Oles",
    author_email="roles@health.ucsd.edu",
    description="Panpiper: snakemake workflow for bacterial isolate analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rolesucsd/Panpiper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",  # Updated to reflect BSD license as mentioned
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 3 - Alpha"],
    python_requires='>=3.5',
    install_requires=[
    "setuptools",
    "biopython>=1.78",
    "pandas>=1.0.0",
    "numpy>=1.19.2",
    "matplotlib>=3.1.0",
    "seaborn>=0.10.0",
    "scikit-learn>=0.22.0",
    "scipy>=1.4.0",
    "scikit-bio>=0.5.6",
    "umap-learn>=0.4.0",
    "dendropy>=4.5.0",
    "PyYAML>=5.3"  # Add PyYAML, adjust version as needed
    ],
    entry_points={
        'console_scripts': ['panpiper=panpiper.main:cli']
    },
    include_package_data=True,
    zip_safe=False,
    package_data={
    'panpiper': [
        'databses/*'
        'databses/*'
        'workflow/*',  # This includes files directly under workflow
        'workflow/envs/*',  # This includes files in the envs subdirectory
        'workflow/scripts/*'  # This includes files in the scripts subdirectory
        ]
    }
)
