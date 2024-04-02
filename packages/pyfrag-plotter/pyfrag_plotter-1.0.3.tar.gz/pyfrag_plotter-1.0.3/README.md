# PyFrag Plotter

[![Documentation](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/build_docs.yml/badge.svg)](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/build_docs.yml) [![Testing](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/test.yml/badge.svg)](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/test.yml)

[![PyPI version](https://badge.fury.io/py/pyfrag-plotter.svg)](https://badge.fury.io/py/pyfrag-plotter) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyfrag-plotter.svg)](https://pypi.python.org/pypi/pyfrag-plotter/) [![PyPI license](https://img.shields.io/pypi/l/pyfrag-plotter.svg)](https://pypi.python.org/pypi/pyfrag-plotter/) [![PyPI status](https://img.shields.io/pypi/status/pyfrag-plotter.svg)](https://pypi.python.org/pypi/pyfrag-plotter/)

## Introduction

The package contains python scripts that can be used to plot the results of pyfrag calculations (see the [PyFrag program](https://pyfragdocument.readthedocs.io/en/latest/install.html)). PyFrag is a program written at the Vrije Universieit Amsterdam to analyze reaction coordinates of reactions using quantum mechanical software. The analysis methods consist of the ["Activation Strain Model"](https://www.nature.com/articles/s41596-019-0265-0) and ["Energy Decomposition Analysis"](https://onlinelibrary.wiley.com/doi/10.1002/9780470125922.ch1). The package is still in development as of 2023 and will be updated regularly.

## Purpose

PyFrag generates a .txt file with the results of the calculations. The format is one (relatively) large table containing energy terms for every point on the intrinsic reaction coordinate (IRC) that has been calculated. The file can be readily exported to software such as Excel or Origin to plot the results. However, this is a tedious process and requires a lot of manual work. This package contains scripts that can be used to plot the results of the calculations. Especially when multiple plots need to be made, and something has to be changed in the end, this package can save a lot of time.

## Installation

There are several ways to install the package. The package is still in development and will be available on PyPI in the future. For now, the package can be installed locally or in a jupyter notebook environment.

- [x] Local: first clone the github page and move to the directory. Then install it locally in your python environment with
``pip install -e .``

- [x] JupyterNotebook: Run the following command in the jupyter notebook:
``!pip install -e .``

- [x] PyPI: ``pip install pyfrag_plotter``

## Simple script

Tutorials covering key functionality can be found in the [example folder](example). The folder contain a plain python script, and a JupyterNotebook script with more explanations. The [simple script](example/example_pyfrag_plotter.py) is a good place to start quickyl. The more [detailed script](example/example_pyfrag_plotter.ipynb) is if you want to know more about how the package works. This script covers the basic functionality of the package and shows how to plot the results of a pyfrag calculation.

## Docs

[Documentation](https://siebelede.github.io/pyfrag_plot/) is available using ReadtheDocs and GitHub Pages. Still in development.

## Authors

Siebe Lekanne Deprez, PhD student at the Vrije Universiteit Amsterdam (VU) working in the theoretical chemistry department.

## License

This package is licensed under the [MIT License](LICENSE.txt).

## How to cite

Lekanne Deprez, S.J., PyFragPlotter, 2023, https://github.com/SiebeLeDe/pyfrag_plot

## How to contribute

Everyone is welcome to contribute to this project. Please do so by making a pull request and/or raising an issue. Preferably, please use the Google Python Style Guide and the Google docstring style when writing code (including docstrings!).

## Dependencies

Please visit the [requirements file](requirements.txt) for a list of dependencies. The whole package is written in a python environment and is compatible for python versions 3.6 and higher.

## Contact Me

If you wish to contact me, please do so by sending an email to [my mail adres](s.j.lekanne.deprez@vu.nl), or by raising an issue on GitHub.

## FAQ

Let me know if there are questions so that I could include this further!
