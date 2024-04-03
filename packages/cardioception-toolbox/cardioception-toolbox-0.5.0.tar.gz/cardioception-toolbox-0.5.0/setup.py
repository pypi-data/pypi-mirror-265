# Copyright (C) 2020 Nicolas Legrand
import os
import codecs
from setuptools import find_packages, setup

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_requirements():
    with codecs.open(REQUIREMENTS_FILE) as buff:
        return buff.read().splitlines()

def get_version(rel_path):
    """Get the package's version number.
    We fetch the version  number from the `__version__` variable located in the
    package root's `__init__.py` file. This way there is only a single source
    of truth for the package's version number.

    """
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

DESCRIPTION = "Cardioception Python Toolbox"
LONG_DESCRIPTION = """Measuring cardiac interoception with Psychopy.
"""

DISTNAME = "cardioception-toolbox"
MAINTAINER = "Nicolas Legrand"
MAINTAINER_EMAIL = "nicolas.legrand@cas.au.dk"

if __name__ == "__main__":

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=read("LICENSE"),
        version=get_version("cardioception/__init__.py"),
        url="https://github.com/LegrandNico/cardioception-toolbox",
        install_requires=get_requirements(),
        include_package_data=True,
        packages=find_packages(),
        package_data={
            "cardioception.HBC": ["*.wav", "*.png"],
            "cardioception.HRD": ["*.wav", "*.png"],
            "cardioception.notebooks": ["*.ipynb"],
        },
    )
