import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

from pybotnet import __github_link__, __version__

# setup to pypi.org :
# python setup.py sdist bdist_wheel
# twine upload  dist/*

# twine upload --repository testpypi dist/*


# Package meta-data.
NAME = "pybotnet"
DESCRIPTION = "A Python framework for building remote control, botnet , trojan or backdoor with Telegram or other control panels"
URL = __github_link__
EMAIL = "onionj98@gmail.com"
AUTHOR = "onionj"
REQUIRES_PYTHON = ">=3.8.0"
VERSION = __version__
KEYWORDS = [
    "onionj pybotnet",
    "python remote control",
    "python backdoor",
    "python botnet",
    "pybotnet",
    "python ddos",
    "python backdoor",
    "python trojan",
    "reverse shell",
    "python keylogger"
    "framework",
]


# What packages are required for this module to be executed?
with open("requirements.txt") as f:
    dependencies = f.read().splitlines()


# What packages are optional?
EXTRAS = {}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))


try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=dependencies,
    extras_require=EXTRAS,
    include_package_data=True,
    license="gpl-3.0",
    keywords=KEYWORDS,
    classifiers=[
        # Again, pick a license
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
