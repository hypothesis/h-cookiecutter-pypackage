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

Publishing to PyPI
------------------

By default when your package passes all tests, coverage, format and linting
requirements, it will be built and uploaded to [https://pypi.org/](https://pypi.org/).

For this to work you'll need to setup an API key for the project.

### Build a package and upload it to PyPI

* Run: `make dist BUILD=0.0`
* Run: `tox -e publish --run-command "twine upload -u eng@list.hypothes.is -p <PASSWORD_HERE> dist/*"`
  
### Create an API key in PyPI  

* Login to [https://pypi.org/](https://pypi.org/)
* Goto "Your projects" and select "Manage" on the correct project
  * "Settings" > "Create a token for <project-name-here>"
  * Use the project name as the name
  * Set the scope to the same project
  * __COPY THE KEY NOW!__ - You __won't__ get another opportunity
* Add the key to Passpack

You may want to add some other personal accounts as owners so that we do not
have a single account as maintainer.

### Add the key to Github as a secret

* Go to [https://github.com/](https://github.com/) and find the correct project
* Go to <kbd>Settings</kbd> > <kbd>Secrets</kbd> > <kbd>Add a new secret</kbd>
* Use "`PYPI_TOKEN`" as the name
* Paste the API key in as the value
* Press <kbd>Add secret</kbd>

Your next successful commit in `master` should now publish to PyPI. 

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
