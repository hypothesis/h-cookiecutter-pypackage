{{ cookiecutter.project_name }}
===============================

{{ cookiecutter.description }}

Features
--------

TBC

Usage
-----

```python
# Usage example
```

Building
--------

Many commands are available via the Makefile. The basic commands available are:

 * `make test` - Run the test suite
 * `make coverage` - Run after running tests to see the coverage
 * `make lint` - Get linter feedback
 * `make format` - Format the project according to Hypothesis standards
 * `make package` - Test packaging locally

For details of other available actions run:

    make help

Installing
----------

Once built, this package can be downloaded directly from PyPi with:

    pip install {{ cookiecutter.project_slug }}
    
You can also install it locally with:

    pip install .
    
You can install a dynamic link to this code for development (so that as the
code changes, your installed code does too) with:

    pip install --editable .
