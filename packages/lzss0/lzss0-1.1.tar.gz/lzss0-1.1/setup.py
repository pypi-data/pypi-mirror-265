from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="lzss0",
    version="1.1",
    author="lvlrk",
    author_email="lvlrk4u@proton.me",
    maintainer="lvlrk",
    maintainer_email="lvlrk4u@proton.me",
    url="https://github.com/lvlrkza/lzss0",
    description="A quick & feature-rich LZSS implementation",
    long_description="A LZSS implementation with extensive configurability and an easy-to-read C backend",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["cython"],
    license="GPLv3",
    license_files=["LICENSE"],
    ext_modules =
        cythonize("lzss0.pyx", compiler_directives=
                  {"language_level": "3"})
)
