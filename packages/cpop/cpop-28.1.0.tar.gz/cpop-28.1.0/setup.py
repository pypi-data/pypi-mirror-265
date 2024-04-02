import os
import shutil

from Cython.Build import cythonize
from setuptools import Command
from setuptools import setup

NAME = "cPop"
SETUP_DIRNAME = os.path.dirname(__file__)


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in ("pop", "hub", "tests"):
            for root, dirs, files in os.walk(
                os.path.join(os.path.dirname(__file__), subdir)
            ):
                for dir_ in dirs:
                    if dir_ == "__pycache__":
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    # dot-delimited list of modules to not package. It's not good to package tests:
    skip_mods = ["tests"]
    for package in ("pop", "hub"):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            modname = pdir.replace(os.sep, ".")
            if modname not in skip_mods:
                modules.append(modname)
    return modules


setup(
    ext_modules=cythonize(os.path.join("pop", "pop.data.pyx")),
    packages=discover_packages(),
    cmdclass={"clean": Clean},
)
