import re
import winreg
import pathlib
import subprocess
from typing import List, Optional
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.browsers_handler.models import Browser
from win32api import (
	GetFileVersionInfo,
	HIWORD,
	LOWORD
)


__all__ = [
	"get_browser_version",
	"get_installed_browsers",
	"get_webdriver_version"
]


def get_webdriver_version(driver_path: PATH_TYPEHINT) -> Optional[str]:
	"""
	Retrieves the version of a given webdriver executable.

	Args:
		driver_path (PATH_TYPEHINT): The path to the webdriver executable. It can be a string or a Path object.

	Returns:
		Optional[str]: The version of the webdriver as a string, or None if the version cannot be determined.

	Raises:
		FileNotFoundError: If the webdriver executable does not exist at the given path.
		Exception: If there is an error executing the webdriver or parsing the output.
	"""
	
	driver_path = pathlib.Path(driver_path)
	
	if not driver_path.exists():
		raise FileNotFoundError(f"{driver_path} not found.")
	
	try:
		process = subprocess.Popen(
				[driver_path, "--version"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
		)
		stdout, stderr = process.communicate()
	
		output = stdout.decode("utf-8").strip()
		error = stderr.decode("utf-8").strip()
	
		if error:
			raise Exception(error)
	
		match = re.search(r"([\d.]+)", output)
		if match:
			return match.group(1)
	
		return None
	except Exception as e:
		raise e


def get_browser_version(browser_path: PATH_TYPEHINT) -> str:
	"""
	Retrieves the version of a browser given its file path.

	This function uses the `GetFileVersionInfo` function from the `win32api` module to extract the browser's version information from the executable file.

	Args:
		browser_path (Path): The file path to the browser executable.

	Returns:
		str: The version of the browser as a string, or "unknown" if the file does not exist.
	"""
	
	browser_path = pathlib.Path(browser_path)
	
	if not browser_path.exists():
		return "unknown"
	
	info = GetFileVersionInfo(str(browser_path.resolve()), "\\")
	
	ms = info["FileVersionMS"]
	ls = info["FileVersionLS"]
	
	return ".".join(map(str, (HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls))))


def get_installed_browsers() -> List[Browser]:
	"""
	Retrieves a List of installed browsers on a Windows system by querying the registry.

	This function iterates through different registry locations to identify installed browsers and their paths.
	It constructs a List of unique `Browser` objects, each representing an installed browser.

	Returns:
		List[Browser]: A List of unique installed browsers.
	"""
	
	installed_browsers = []
	
	for root_key, access in [
		(winreg.HKEY_CURRENT_USER, winreg.KEY_READ),
		(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_READ | winreg.KEY_WOW64_64KEY),
		(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
	]:
		with winreg.OpenKey(root_key, r"SOFTWARE\Clients\StartMenuInternet", access=access) as key:
			num_subkeys = winreg.QueryInfoKey(key)[0]
	
			for i in range(num_subkeys):
				try:
					subkey = winreg.EnumKey(key, i)
	
					browser_name = winreg.QueryValue(key, subkey)
					if not browser_name or not isinstance(browser_name, str):
						browser_name = subkey
	
					with winreg.OpenKey(key, rf"{subkey}\shell\open\command") as subkey:
						browser_path = pathlib.Path(winreg.QueryValue(subkey, None).strip('"'))
	
						if not browser_path.exists():
							continue
	
						found_browser = Browser(
								name=browser_name,
								path=browser_path,
								version=get_browser_version(browser_path)
						)
	
						if found_browser not in installed_browsers:
							installed_browsers.append(found_browser)
				except (OSError, AttributeError, TypeError, ValueError, FileNotFoundError):
					pass
	
	return installed_browsers
