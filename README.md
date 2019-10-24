# h-cookiecutter-pypackage

A [Cookiecutter](https://cookiecutter.readthedocs.io/) project template for
creating Hypothesis-style Python packages. Automates the creation and updating
of all our Python package project tooling and scaffolding: `Makefile`,
`tox.ini`, `setup.py`, GitHub Actions, etc.

Usage
-----

### You will need

* [Cookiecutter](https://cookiecutter.readthedocs.io/)
  (`pip install cookiecutter`, `brew install cookiecutter` or `sudo apt install
  cookiecutter`)

### Creating a new project

To create a new project from this template:

```terminal
$ cookiecutter gh:hypothesis/h-cookiecutter-pypackage
```

Hacking
-------

### Installing h-cookiecutter-pypackage in a development environment

#### You will need

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  Follow the instructions in the pyenv README to install it.
  The Homebrew method works best on macOS.
  On Ubuntu follow the Basic GitHub Checkout method.

#### Clone the git repo

```terminal
$ git clone https://github.com/hypothesis/h-cookiecutter-pypackage.git
```

This will download the code into a `h-cookiecutter-pypackage` directory in your
current working directory. You need to be in the `h-cookiecutter-pypackage`
directory for the rest of the installation process:

```terminal
$ cd h-cookiecutter-pypackage
```

#### Run the tests

```terminal
$ make test
```

**That's it!** You’ve finished setting up your h-cookiecutter-pypackage
development environment. Run `make help` to see all the commands that're
available for linting, code formatting, packaging, etc.
