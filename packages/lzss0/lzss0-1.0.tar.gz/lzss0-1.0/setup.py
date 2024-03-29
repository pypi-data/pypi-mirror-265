from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="lzss0",
    version="1.0",
    author="lvlrk",
    author_email="lvlrk4u@proton.me",
    description="A quick & feature-rich LZSS implementation",
    packages=find_packages(),
    python_requires=">=3.0",
    ext_modules =
        cythonize("lzss0.pyx", compiler_directives=
                  {"language_level": "3"})
)
