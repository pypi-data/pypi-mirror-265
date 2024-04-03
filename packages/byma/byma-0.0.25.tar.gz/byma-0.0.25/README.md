# ByMa

ByMa is a Python package designed to facilitate numerical mathematics tasks by implementing a range of standard methods, from iterative techniques to bifurcation methods. Noted for its simplicity, clarity, and efficiency, ByMa aims to enhance the learning experience for newcomers to numerical mathematics while streamlining the implementation and utilization of popular scientific libraries such as NumPy, SciPy, and Matplotlib.


## Installation

ByMa is best installed in a [virtual environment](https://docs.python.org/3/library/venv.html).
We state the most common steps for creating and using a virtual environment here.
Refer to the documentation for more details.

To create a virtual environment run
```
python3 -m venv /path/to/new/virtual/environment
```

and to activate the virtual environment, run
```
source /path/to/new/virtual/environment/bin/activate
```

After this, we can install ByMa from the pip package by using
```
pip install byma
```

In case the dependencies are not installed, you can run 
```
pip install -e .
```

## Packages

ByMa consists of several subpackages, each serving a distinct purpose:

- **nuby**: Numerical Bifurcation Analysis Tools
- **iteral**: Tools for iterative algorithms
- **pyplot**: Tools for plotting functions
- **interface**: Interface functionalities

## Authors

* Lorenzo Zambelli [website](https://lorenzozambelli.it)