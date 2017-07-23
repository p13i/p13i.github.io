---
layout: posts/post
author: Pramod Kotipalli
title:  Testing Python Packages
subtitle: Integration with tox and Travis CI
categories:
    - programming
    - python
    - tools
    - testing
    - continuous-integration
    - tox
    - travis-ci

---

**Completed project**: [![GitHub](https://github.com/favicon.ico)](https://github.com/p13i/pytouch/tree/v0.0.2) [![Travis CI](https://cdn.travis-ci.org/images/favicon.png)](https://travis-ci.org/p13i/pytouch)

In my [previous post]({% post_url 2017-07-11-python-command-line-tools %}), we developed a simple Python package that creates a file, somewhat similar to the `touch` found in Linux systems.
```bash
$ pytouch new-file.txt
$ ls
  [...]
  new-file.txt
  [...]
```
Explore the code from the previous post at tag `v0.0.1` [here](https://github.com/p13i/pytouch/tree/v0.0.1). You can clone the code and follow along as we explore `tox` and Travis CI in this post:
```bash
$ git clone https://github.com/p13i/pytouch.git
& cd pytouch
$ git checkout tags/v0.0.1 -b my-follow-along
```
Now, you'll have the `pytouch` code at `v0.0.1` ready to follow along on the new `my-follow-along` branch.

# Testing `pytouch`

Python packages don't come packaged with an expressly-specified Python interpreter. So, our package will need to rely on our end users' interpreter. As such, we need to ensure that our package will work on multiple different platforms without issue.

[`tox`](https://tox.readthedocs.io/en/latest/) is a Python tool designed expressly for solving this problem. With `tox`, we can easily specify multiple version of Python for which `tox` then creates a virtual environment to run Python tests.

Before exploring `tox`, we'll need to address some prerequisites and author the tests that `tox` will run.

## Prerequisites

Before continuing, let's create a `.gitignore` file so that we don't accidentally commit system-specific or auto-generated files. Please see the [diff](https://github.com/p13i/pytouch/commit/588c0a84ed0ab6b320927d9bf1f38cba16546b69) for new `.gitignore` file's contents.

In the [previous post]({% post_url 2017-07-11-python-command-line-tools %}), I made a small typo that we can quickly fix. On line 6 of `pytouch/pytouch.py` please change the `3` to `2`:
```python
6    if len(sys.argv) != 2:
                         ^
```

## Authoring tests using `unittest` and `mock`

Next, we want to actually create the tests that will ensure our `main` method in `pytouch/pytouch.py` is working properly.

Create a new file called `tests.py` in the root of the project. Fill in the file with [this](https://github.com/p13i/pytouch/blob/v0.0.2/tests.py).

Assuming you are familiar with Python's [`unittest` framework](https://docs.python.org/2/library/unittest.html), let's discuss a few lines in particular:

- `tests.py:17` : `@mock.patch.object(sys, 'argv', ['pytouch'])`

    This [method decorator](https://www.python.org/dev/peps/pep-0318/) alters the `sys.argv` list to be `['pytouch']` for the scope of the succeeding method starting on `tests.py:6`: `def test_not_enough(self):`

- `tests.py:23` : `self.assertRaises(ValueError, main)`

    Because of the method decorator on line 17, the `main` function will not have access to a `sys.argv` list of length two causing [this check](https://github.com/p13i/pytouch/blob/v0.0.2/pytouch/pytouch.py#L6) to fail. Thus, we expect a [`ValueError`](https://github.com/p13i/pytouch/blob/v0.0.2/pytouch/pytouch.py#L6) to be raised.

## Adding dependencies

You may have noticed that the [`import mock`](https://github.com/p13i/pytouch/blob/v0.0.2/tests.py#L6) statement in `tests.py` is not a standard, in-built Python module; it's located on [`PyPI`](https://pypi.python.org/pypi) and can be installed using `pip install mock`. But how can we ensure that our package has access to this library?

We can specify it as a dependency in our `setup.py`. Simply insert `install_requires=['mock']` in the `setup` method of `setup.py` and you should be good to go. See the [completed `setup.py`](https://github.com/p13i/pytouch/blob/v0.0.2/setup.py#L11-L14) to double-check your work.

## Running tests

Now, we can finally run our tests!

```bash
$ python setup.py test
running test

[...]

test_not_enough (tests.TestMainBadArgs) ... ok
test_too_many (tests.TestMainBadArgs) ... ok
test_too_many (tests.TestMainGoodArgs) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

## `tox` integration

Now, we're finally ready to test our module across multiple versions of the Python interpreter.

Create a file named `tox.ini` (you could use our tool `pytouch tox.ini`!). Add the following five lines to the file:
```ini
[tox]
envlist = py26,py27,py33,py34,py35,py36

[testenv]
commands = python setup.py test
```
The `envlist` specifies the list of Python interpreters to run the `python setup.py test` command in. Here, `py26` indicates a Python v2.6.x interpreter, `py27` indicates a Python v2.7.x interpreter, etc.

Install `tox` on your system or in a [`virtualenv`](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) and run:
```bash
$ tox --skip-missing-interpreters
```

Because our host operating system may not contain all of six versions of Python specified in `envlist`, we provide the `--skip-missing-interpreters` flag so `tox` won't fail when it doesn't find a particular interpreter.

At the end of a rather long console output, you'll see
```bash
    py26: commands succeeded
    py27: commands succeeded
SKIPPED:  py33: InterpreterNotFound: python3.3
SKIPPED:  py34: InterpreterNotFound: python3.4
SKIPPED:  py35: InterpreterNotFound: python3.5
    py36: commands succeeded
    congratulations :)
```
indicating that our tool works for the specific Python interpreters available on the host system. In this case, you can see that my OS has Python 2.6, Python 2.7, and Python 3.6 installed. The lack of Python 3.3, 3.4, and 3.5 causes those iterations to be skipped by `tox`.

But, you may note, we *must* test our tool on all versions of Python! We don't know what our users will be using!

## Running `tox` tests on multiple interpreters

We have a few options here:

1. Install all six Python interpreters on one machine. (Sounds like a bad idea!)
2. Use a container or virtual machine solution like Docker or Vagrant to manage an environment with multiple interpreters.
3. Use a solution like Travis CI to run our tests in multiple environments on a managed cloud.

### Running all `tox` tests with Docker

If you're familiar with Docker (or want to see how this option works), continue on. If not, please move on to the Travis CI section below.

I created a [Docker image](https://github.com/p13i/docker-tox/blob/master/Dockerfile) with all six of these interpreters installed so we can simply pull the ~500 MB image instead of installing each one by hand and risking all sorts of unintended consequences. First, pull the image:
```bash
docker pull p13i/docker-tox
```

Now, within our main `pytouch` directory, we can simply run
```bash
$ docker run \
    --rm \
    --volume $(pwd):/app \
    --workdir /app \
    p13i/docker-tox \
    tox
```
to run our `tox` tests on all six specified interpreters.

Note that we didn't pass in the `--skip-missing-interpreters` flag because this Docker image comes with all six of these interpreters installed.

### Running tox tests on Travis CI

[Travis CI](https://travis-ci.org/) is a great, free tool for running tests for open-source projects.

Create a file named `.travis.yml`:
```yml
language: python

# These are all the different versions we want to run our tests with
python:
  - "2.6"
  - "2.7"
  - "3.3"
  - "3.4"
  - "3.5"
  - "3.6"

# Install this package to easily run tox in all these environments on Travis
install: pip install tox-travis

# The test script (as run locally)
script: tox
```

Commit your changes and upload to your own git repository (or simply [fork](https://github.com/p13i/pytouch/fork) the existing one). After setting up your repository with Travis, you'll [see all our tests running](https://travis-ci.org/p13i/pytouch) on all six of these interpreters. From Travis, you can also get a status badge that will help our users know that our tool works properly: [![Build Status](https://travis-ci.org/p13i/pytouch.svg?branch=master)](https://travis-ci.org/p13i/pytouch)

Best of luck writing your own Python-based command line tools!

# Further steps

In my next post, I'll show you how to upload Python packages to the official Python package index [`PyPI`](https://pypi.python.org/pypi).
