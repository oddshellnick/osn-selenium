import pathlib
from typing import List

from setuptools import find_packages, setup


def get_long_description() -> str:
	long_description_path = pathlib.Path("README.md")
	
	if long_description_path.is_file():
		return open(long_description_path, "r", encoding="utf-8").read()

	raise FileNotFoundError("README.md not found")


def get_install_requires() -> List[str]:
	requirement_path = pathlib.Path("requirements.txt")
	
	if requirement_path.is_file():
		return open(requirement_path, "r", encoding="utf-8").read().splitlines()

	raise FileNotFoundError("requirements.txt not found")


def get_description() -> str:
	description_path = pathlib.Path("description.txt")
	
	if description_path.is_file():
		return open(description_path, "r", encoding="utf-8").read()

	raise FileNotFoundError("description.txt not found")


setup(
		name="osn-selenium",
		version="1.0.0-beta.6",
		author="oddshellnick",
		author_email="oddshellnick.programming@gmail.com",
		description=get_description(),
		long_description=get_long_description(),
		long_description_content_type="text/markdown",
		packages=find_packages(exclude=["unit_tests*"]),
		install_requires=get_install_requires(),
		package_data={"osn_selenium": ["javascript/scripts/*.js"]},
		include_package_data=True,
)
