import sys
import pathlib
from typing import List, Optional
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.browsers_handler.models import Browser
from osn_selenium.exceptions.platform import (
	PlatformNotSupportedError
)


__all__ = [
	"get_installed_browsers",
	"get_path_to_browser",
	"get_version_of_browser",
	"get_version_of_driver"
]

if sys.platform == "win32":
	from osn_selenium.browsers_handler._windows import (
			get_installed_browsers as _platform_get_installed_browsers,
			get_webdriver_version as _platform_get_webdriver_version
	)
elif sys.platform == "linux":
	from osn_selenium.browsers_handler._linux import (
			get_installed_browsers as _platform_get_installed_browsers,
			get_webdriver_version as _platform_get_webdriver_version
	)
else:
	raise PlatformNotSupportedError(platform=sys.platform)


def get_version_of_driver(driver_path: PATH_TYPEHINT) -> Optional[str]:
	"""
	Retrieves the version of a given webdriver executable based on the current platform.

	Args:
		driver_path (PATH_TYPEHINT): The path to the webdriver executable.

	Returns:
		Optional[str]: The version of the webdriver as a string, or None if not determined.
	"""
	
	return _platform_get_webdriver_version(driver_path=driver_path)


def get_installed_browsers() -> List[Browser]:
	"""
	Retrieves a List of installed browsers on the system.

	This function detects and lists the browsers installed on the operating system.
	It supports different operating systems and uses platform-specific methods to find installed browsers.

	Returns:
		List[Browser]: A List of installed browsers. Each item in the List is a dictionary of type `Browser` containing information about the browser like name, version, and path.

	Raises:
		PlatformNotSupportedError: If the operating system is not supported.
	"""
	
	return _platform_get_installed_browsers()


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
		if browser.name == browser_name:
			return browser.version
	
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
		if browser.name == browser_name:
			return browser.path
	
	return None
