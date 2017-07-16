---
layout: posts/post
author: Pramod Kotipalli
title:  Building Command Line Tools with Python
subtitle: Python Makes CLIs Easier!
categories:
    - programming
    - python
    - tools
    -

---

**Completed project**: [![GitHub](https://github.com/p13i/pytouch/tree/v0.0.1)

Unix has a command `touch` which is commonly used to create files. Let's create a Python program with similar functionality that can be called as if it were a built-in Unix command.

---

# `pytouch`

Here begins the story of our CLI tool `pytouch`. For simplicity, let's let `pytouch` only take one argument `filename`.

When we enter `pytouch sample.txt`, we should expect to create a new file called `sample.txt`. If such a file already exists, we'll truncate it.

## Installation method

We'll Python's in-built `setuptools` to allow our tool to be installed with `pip`, the standard package management tool for Python.

## Python version compatibility

When we distribute a command line tool like this, we only know that our user has installed Python; we don't know what version of Python is installed or what packages are available to us. We'll use `tox` to ensure that our tool can run on several different machines.

## Directory structure

Let's create a directory called `pytouch-tool` which will house all of our code. Create files until your folder structure looks like:

```
pytouch-tool
+-- pytouch
|   +-- __init__.py
|   +-- pytouch.py
+-- setup.py
```

### Inside `pytouch/pytouch.py`

This file will contain the `main` method of our tool. It'll handle parsing the one `filename` argument and creating that file in the current working directory. Add this to `pytouch/pytouch.py`:

``` python
import sys

def main():
    # sys.argv[0] is the path to the python interpreter
    # sys.argv[1] should contain the name of the file we want to create
    if len(sys.argv) != 3:
        raise ValueError("Please provide the name of the file to create.")

    filename = sys.argv[1]

    # 'w+' erases the file if it exists and creates it if the file doesn't exist
    with open(filename, 'w+'):
        pass
```

I hope this code is pretty self explanatory.

### Inside `pytouch/__init__.py`

We'll keep this file blank. This is just Python's way of knowing that it should treat the containing `pytouch` folder as a Python package. It's important to treat the `pytouch` directory as a package as we'll see next.

### Inside `setup.py`

We're going to fill out this file so that we can use `pip` to simply install this package. Add the following to `setup.py`:

``` python
from setuptools import setup

setup(
    # The name of our pip package
    name='pytouch',
    # The Python packages in this project
    packages=[
        # This is the `pytouch` folder that contains __init__.py and pytouch.py
        'pytouch',
    ],
    version="0.0.1",
    entry_points={
        'console_scripts': [
            # We use this line to map our `main()` method in pytouch.py
            # to a shell command `pytouch`
            'pytouch = pytouch.pytouch:main',
        ],
    },
)
```

Learn more about the `setuptools` package [here](https://setuptools.readthedocs.io/en/latest/setuptools.html).

---

## Installation

Go to the root of our project, the `pytouch-tool` directory. `pip` documentation tells us that we can run `pip install .` to install our package. You should see output like

```
Processing /path/to/pytouch-tools
Installing collected packages: pytouch
  Running setup.py install for pytouch ... done
Successfully installed pytouch-0.0.1
```


Now, if you run `pip freeze | grep pytouch`, you should see our tool!

```shell
$ pip freeze | grep pytouch
...
pytouch==0.0.1
...
```

## Running `pytouch`

Take 'er for a spin!

```shell
$ pytouch sample.txt
$ ls
...
sample.txt
...
```

## Un-installation

Run `pip uninstall pytouch` and our tool is removed.

---

# Further Steps

In a soon to come future post, we'll dive into testing tools that will ensure our project can work with any version of Python.
