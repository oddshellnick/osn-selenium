import sys
import pathlib
from typing import Optional
from osn_selenium.browsers_handler.types import Browser
from osn_selenium.errors import (
	PlatformNotSupportedError
)
from osn_selenium.browsers_handler._windows import (
	get_installed_browsers_win32
)


def get_installed_browsers() -> list[Browser]:
	"""
	Retrieves a list of installed browsers on the system.

	This function detects and lists the browsers installed on the operating system.
	It supports different operating systems and uses platform-specific methods to find installed browsers.

	Returns:
		list[Browser]: A list of installed browsers. Each item in the list is a dictionary of type `Browser` containing information about the browser like name, version, and path.

	Raises:
		PlatformNotSupportedError: If the operating system is not supported.
	"""
	
	if sys.platform == "win32":
		return get_installed_browsers_win32()
	else:
		raise PlatformNotSupportedError(sys.platform)


def get_version_of_browser(browser_name: str) -> Optional[str]:
	"""
	Retrieves the version of a specific installed browser.

	This function searches for an installed browser by its name and returns its version if found.

	Args:
		browser_name (str): The name of the browser to find the version for (e.g., "Chrome", "Firefox").

	Returns:
		Optional[str]: The version string of the browser if found, otherwise None.
	"""
	
	for browser in get_installed_browsers():
		if browser["name"] == browser_name:
			return browser["version"]
	
	return None


def get_path_to_browser(browser_name: str) -> Optional[pathlib.Path]:
	"""
	Retrieves the installation path of a specific installed browser.

	This function searches for an installed browser by its name and returns its installation path as a pathlib.Path object if found.

	Args:
		browser_name (str): The name of the browser to find the path for (e.g., "Chrome", "Firefox").

	Returns:
		Optional[pathlib.Path]: The pathlib.Path object representing the browser's installation path if found, otherwise None.
	"""
	
	for browser in get_installed_browsers():
		if browser["name"] == browser_name:
			return browser["path"]
	
	return None
