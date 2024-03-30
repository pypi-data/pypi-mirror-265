from pathlib import Path
from setuptools import setup, find_packages

NAME = "pyloudnorm_custom_package"
DESCRIPTION = "Implementation of ITU-R BS.1770-4 loudness algorithm in Python"
EMAIL = "kscreamsun@gmail.com"
AUTHOR = "kcode"
REQUIRES_PYTHON = ">=3.0"
VERSION = "0.1.0"

HERE = Path(__file__).parent

try:
    with open(HERE / "README.md", encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=["pyloudnorm_custom_package"],
    install_requires=["numpy>=1.14.2"],
    include_package_data=True,
    license="MIT"
)
