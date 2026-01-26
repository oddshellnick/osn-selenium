from typing import Union
from osn_selenium._cdp_import import (
	check_cdp_version_exists_on_github
)


__all__ = ["CDPPackageError", "DependencyError"]

_CDP_PACKAGE_EXISTS = """
CDP package for {version} is not installed.
Fix: Run the following command:
\t`pip install git+https://github.com/oddshellnick/osn-selenium-cdp.git@{version}`
""".strip("\n")

_CDP_PACKAGE_NOT_EXISTS = """
CDP package for version {version} was not found on GitHub or locally.
Please check available versions at: https://github.com/oddshellnick/osn-selenium-cdp
If you need this specific version, you can generate it using the https://github.com/oddshellnick/selenium-package-parser tool.
""".strip("\n")


class DependencyError(Exception):
	"""
	Base exception for dependency-related issues.
	"""
	
	pass


class CDPPackageError(DependencyError):
	"""
	Exception raised when a required CDP package is missing.
	"""
	
	def __init__(self, version: Union[int, str]):
		"""
		Initializes the error with version details.

		Args:
			version (Union[int, str]): The missing CDP version.
		"""
		
		self.version = version if isinstance(version, str) else f"v{version}"
		
		super().__init__(self._generate_report())
	
	def _generate_report(self) -> str:
		"""
		Generates a detailed error message checking remote availability.

		Returns:
			str: Formatted error message with instructions.
		"""
		
		version_exists_on_github = check_cdp_version_exists_on_github(version=self.version)
		
		if version_exists_on_github:
			return _CDP_PACKAGE_EXISTS.format(version=self.version)
		
		return _CDP_PACKAGE_NOT_EXISTS.format(version=self.version)
