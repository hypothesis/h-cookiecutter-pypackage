from setuptools import find_packages, setup

from setup_extra import Package

package = Package(name="h_cookiecutter_pypackage", version="1.0")

INSTALL_REQUIRES = []

TESTS_REQUIRE = INSTALL_REQUIRES + ["cookiecutter", "pytest", "coverage", "twine"]


setup(
    # Metadata
    # https://docs.python.org/3/distutils/setupscript.html#additional-meta-data
    name=package.name,
    version=package.get_version(),
    description="",
    long_description=package.read_string("README.md"),
    long_description_content_type="text/markdown",
    author="Hypothesis Engineering Team",
    author_email="eng@list.hypothes.is",
    maintainer="Hypothesis Engineering Team",
    maintainer_email="eng@list.hypothes.is",
    url="https://web.hypothes.is/",
    project_urls={"Source": "https://github.com/hypothesis/h-cookiecutter-pypackage"},
    # From: https://pypi.org/pypi?:action=list_classifiers
    classifiers=[
        # Maybe if we want to put people off less we can change this
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
    ],
    license="License :: OSI Approved :: BSD License",
    platforms=["Operating System :: OS Independent"],
    # Contents and dependencies
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    # Add support for pip install .[test]
    extras_require={"tests": TESTS_REQUIRE},
    # Adding pytest support for `python setup.py test` (also see setup.cfg)
    test_suite="tests",
    setup_requires=[
        "pytest-runner",
        # Try and prevent long-description bug when uploading to PyPI
        "setuptools>=38.6.0",
        "wheel>=0.31.0",
        "twine>=1.11.0",
    ],
    tests_require=TESTS_REQUIRE,
)
