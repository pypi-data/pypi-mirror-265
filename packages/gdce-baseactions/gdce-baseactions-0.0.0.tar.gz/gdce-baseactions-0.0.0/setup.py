import setuptools
from pathlib import Path

setuptools.setup(
    name="gdce-baseactions", # Must be unique name not conflict with package available in pypi repository.
    vesion='1.0.0',
    long_description=Path("README.md").read_text(),
    packages=['baseOperation', 'data', 'baseOperation/inputFiles', 'baseOperation/Outputfiles', 'baseOperation/static']
    # package=setuptools.find_packages() # find all packages except test and data.
)