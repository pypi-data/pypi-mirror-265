import setuptools 
import pathlib

setuptools.setup(
    name='wfmplan',
    version='0.2.0',
    packages=setuptools.find_packages(),
    description = " library for creating workforce plans based on service level agreements (SLAs) and traffic analysis",
    author="Rishi Laddha",
    author_email="laddha.rishi@gmail.com",
    license="MIT",
    install_requires = ["pandas"],
    python_requires = ">=3.10",
)
