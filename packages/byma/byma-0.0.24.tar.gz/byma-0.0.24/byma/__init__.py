"""
ByMa: A scientific computing package for Python
================================================

Documentation is available in the docstrings and
online at 

Subpackages
-----------
Using any of these subpackages requires an explicit import. For example,
``import byma.nuby``.

::

 nuby                         --- Numerical Bifurcation Analysis Tools
 iteral                       --- Tools for iterative algorithms
 pyplot                       --- Tools for plotting functions
 interface

Public API in the main ByMa namespace
--------------------------------------
::

 __version__       --- ByMa version string
 test              --- Run ByMa unittests

"""

import importlib as _importlib

submodules = [
    'nuby',
    'iteral',
    'pyplot',
]

__all__ = submodules + [
    'test',
    '__version__',
]


def __dir__():
    return __all__


def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'byma.{name}')
    else:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(
                f"Module 'byma' has no attribute '{name}'"
            )