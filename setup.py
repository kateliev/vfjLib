import re
import sys
from codecs import open
from os import path

from setuptools import find_packages, setup

folderLib = "Lib"
packageName = find_packages(folderLib)[0]


def get_version(*args):
    verpath = (folderLib, packageName, "__init__.py")
    verstrline = open(path.join(*verpath)).read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    else:
        return "undefined"


def get_absolute_path(*args):
    """Transform relative pathnames into absolute pathnames."""
    directory = path.dirname(path.abspath(__file__))
    return path.join(directory, *args)


def get_description(*args):
    readmepath = get_absolute_path("README.md")
    if path.exists(readmepath):
        long_description = open(readmepath, encoding="utf-8").read()
    else:
        long_description = ""
    return long_description


def get_requirements(*args):
    """Get requirements from pip requirement files."""
    requirements = set()
    with open(get_absolute_path(*args)) as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


needs_pytest = {"pytest", "test"}.intersection(sys.argv)
pytest_runner = ["pytest_runner"] if needs_pytest else []
needs_wheel = {"bdist_wheel"}.intersection(sys.argv)
wheel = ["wheel"] if needs_wheel else []

setup(
    name=packageName,
    version=get_version(),
    description="Low-level reader and writer for FontLab JSON (VFJ) font source files",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/kateliev/vfjLib",
    download_url="https://github.com/kateliev/vfjLib/archive/master.zip",
    author="Vassil Kateliev",
    author_email="vassil@kateliev.com",
    license="LICENSE",
    classifiers=[
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=["opentype", "font", "fontlab", "vfj"],
    package_dir={"": folderLib},
    packages=[packageName],
    include_package_data=True,
    setup_requires=pytest_runner + wheel,
    tests_require=[
        "pytest>=2.8",
    ],
    python_requires=">=2.7",
    install_requires=get_requirements("requirements.txt"),
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #    'console_scripts': [
    #        'vfj=vfjLib:main',
    #    ],
    # },
)
