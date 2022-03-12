# TypeTyp
A Python-Module to parse some `typing` type-hints into English sentences

## Supported Types
- `Union`
- `Optional`
- `Dict`
- `List`
- `Tuple`

These are the typing classes I use most frequently.
I normally use the built-in Python classes `str`, `float`, `int` etc., in generics.
So this module uses the same approach.

## Idea behind the module
Especially for beginners, the standard Python-Typehints can be potentially challenging to read.
So for educative purposes, it can be helpful to have a little tool that translates the type hints 
of a method, so someone unfamiliar with the Python typing schema can read them. 

## What this module is not supposed to be
This module is just supplementary and is not meant to substitute
fully-fledged Docstrings or the usual type hints.
As shown in the example notebook, the resulting type-tips are focused on the types of each of the method's in- and output parameters but don't provide any contextual information on how the parameter is used in the function.

## Installation
To build the package locally you can run `make install` at the root of the Repository.
This will start a fresh virtual environment with the `typetyp`-package installed.
To run the notebooks you can run `make install-jupyter` to install `ipykernel` to the virtual 
environment as well.
Then you can use the virtual environment as a Jupyter-Kernel.

