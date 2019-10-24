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
    
Updating boilerplate
--------------------

The config and other boilerplate files in this project can be updated by running:

    make template

This will read the `.cookiecutter.json` file and replay the templated files, 
overwriting local changes.

If you would like a particular file to be preserved you can add it
to: `"options.disable_replay"` in the `.cookiecutter.json` file. You can also
just not commit the changes made if you don't like them.

If you would like to update a file that is mentioned in `disable_replay`,
just delete it and it will be replaced when running `make template`.