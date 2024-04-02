from setuptools import setup, find_packages
import re


with open("README.md", "r") as f:
    long_description = f.read()


with open("opplast/__init__.py") as f:
    version = re.search(
        r"""^__version__\s*=\s*['"]([^\'"]*)['"]""", f.read(), re.MULTILINE
    ).group(1)


setup(
    name="opplast-v2",
    version=version,
    author="OwOHamper",
    author_email="barca.teo@gmail.com",
    description="Upload videos to YouTube using geckodriver, Firefox profiles and Selenium.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/OwOHamper/opplast",
    download_url="https://github.com/OwOHamper/opplast/tarball/v" + version,
    packages=["opplast"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["selenium<4"],
    python_requires=">=3.6",
)
