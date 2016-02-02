.. _introduction:

Introduction
============

.. currentmodule:: slactrac

This is the documentation for a Python package designed to make scientific data analysis easier. The main objective is to create a collection of interconnected methods frequently needed to visualize and analyze data using Numpy, Scipy, Matplotlib, and PyQt.

Prerequisites
-------------

Python 3
^^^^^^^^

:mod:`slactrac` works with Python 3 and up, which should be installed via apt-get on \*nix, `Macports <https://www.macports.org/>`_ on Apple machines, or downloaded from https://www.python.org/downloads/.

NumPy and SciPy
^^^^^^^^^^^^^^^

:mod:`slactrac` depends on `NumPy <http://www.numpy.org/>`_ and `SciPy <http://www.scipy.org/>`_ to manipulate data.

`NumPy <http://www.numpy.org/>`_ has dependencies such as BLAS, LAPACK, and ATLAS, which makes downloading building form source is difficult. Installation via apt-get or `Macports <https://www.macports.org/>`_ is highly recommended in order to handle these dependencies. It is possible to `download <http://www.scipy.org/scipylib/download.html>`_ or to `build from source <http://www.scipy.org/scipylib/building/index.html#building>`_.

`SciPy <http://www.scipy.org/>`_ is similar to `NumPy <http://www.numpy.org/>`_, and it is usually easiest to install the two at the same time - they have nearly identical install methods, to the point that at times it is difficult to tell the two apart. It is easiest to follow the `install instructions <http://www.scipy.org/install.html>`_.

Periodictable
^^^^^^^^^^^^^

The :mod:`slactrac.PWFA` module depends on the periodic table for ion masses. This can be installed simply via pip::

        pip install periodictable

Options - Elegant Integration
-----------------------------

Since :mod:`slactrac` replicates many features of `Elegant <http://www.aps.anl.gov/Accelerator_Systems_Division/Accelerator_Operations_Physics/software.shtml#elegant>`_, and interface to simulations was derived. This feature, which is not imported by default, has several of its own prerequisites.

Elegant
^^^^^^^

`Elegant <http://www.aps.anl.gov/Accelerator_Systems_Division/Accelerator_Operations_Physics/software.shtml#elegant>`_ does not have a particularly easy way to install. It is highly recommended to use the binaries hosted at its site. Compilation of source is involved, to say the least, and each iteration tends to bring fresh difficulties. Compiling Elegant is outside the scope of this document.

Python SDDS
^^^^^^^^^^^

As far as I know, only OS X and Windows are supported by `Python SDDS <http://www.aps.anl.gov/Accelerator_Systems_Division/Accelerator_Operations_Physics/software.shtml#PythonBinaries>`_. This is needed to interface with `Elegant's <http://www.aps.anl.gov/Accelerator_Systems_Division/Accelerator_Operations_Physics/software.shtml#elegant>`_ input and output files.

Jinja2
^^^^^^

:mod:`slactrac` depends on `Jinja2 <http://jinja.pocoo.org/>`_ in order to interface with Elegant's configuration files via this module. It can be installed by pip::

        pip install Jinja2
