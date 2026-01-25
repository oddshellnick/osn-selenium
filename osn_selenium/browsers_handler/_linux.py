import os
import re
import glob
import shutil
import pathlib
import subprocess
from osn_selenium._typehints import PATH_TYPEHINT
from typing import (
	List,
	Optional,
	Set,
	Tuple
)
from osn_selenium.browsers_handler.models import Browser
from osn_selenium.exceptions.path import (
	BrowserExecutableNotFoundError
)


__all__ = [
	"get_browser_version",
	"get_installed_browsers",
	"get_webdriver_version"
]


def _get_process_version(executable_path: PATH_TYPEHINT) -> Optional[str]:
	"""
	Executes a process with the --version flag and extracts the version string.

	Args:
		executable_path (PATH_TYPEHINT): The file system path to the executable.

	Returns:
		Optional[str]: The extracted version string if successful, otherwise None.
	"""
	
	executable_path = pathlib.Path(executable_path)
	
	if not executable_path.exists():
		return None
	
	try:
		process = subprocess.Popen(
				[str(executable_path), "--version"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
		)
		stdout, stderr = process.communicate()
	
		output = (stdout.decode("utf-8") + stderr.decode("utf-8")).strip()
	
		match = re.search(r"(\d+(?:\.\d+)+)", output)
	
		if match:
			return match.group(1)
	
		return None
	except (Exception,):
		return None


def get_webdriver_version(driver_path: PATH_TYPEHINT) -> Optional[str]:
	"""
	Retrieves the version string of a WebDriver executable.

	Args:
		driver_path (PATH_TYPEHINT): The path to the WebDriver binary.

	Returns:
		Optional[str]: The version string if found, otherwise None.

	Raises:
		BrowserExecutableNotFoundError: If the provided driver path does not exist.
	"""
	
	driver_path = pathlib.Path(driver_path)
	
	if not driver_path.exists():
		raise BrowserExecutableNotFoundError(path=driver_path)
	
	version = _get_process_version(executable_path=driver_path)
	
	if version:
		return version
	
	return None


def get_browser_version(browser_path: PATH_TYPEHINT) -> str:
	"""
	Retrieves the version string of a browser executable.

	Args:
		browser_path (PATH_TYPEHINT): The path to the browser binary.

	Returns:
		str: The version string or 'unknown' if extraction fails.
	"""
	
	return _get_process_version(executable_path=browser_path) or "unknown"


def _get_browser_from_binary(browser_name: str, binary_name: str, processed_paths: Set[pathlib.Path]) -> Optional[Tuple[Browser, pathlib.Path]]:
	"""
	Attempts to locate a browser binary and create a Browser model.

	Args:
		browser_name (str): The display name of the browser.
		binary_name (str): The command or path used to execute the browser.
		processed_paths (Set[pathlib.Path]): A set of already identified paths to avoid duplicates.

	Returns:
		Optional[Tuple[Browser, pathlib.Path]]: A tuple containing the Browser model and its resolved path.
	"""
	
	full_path = shutil.which(binary_name)
	
	if full_path:
		path_obj = pathlib.Path(full_path)
	
		if path_obj in processed_paths:
			return None
	
		version = get_browser_version(browser_path=path_obj)
	
		browser = Browser(name=browser_name, path=path_obj, version=version)
	
		return browser, path_obj
	
	return None


def get_installed_browsers() -> List[Browser]:
	"""
	Scans the Linux system for installed web browsers.

	Returns:
		List[Browser]: A list of detected Browser instances.
	"""
	
	found_browsers: List[Browser] = []
	processed_paths: Set[pathlib.Path] = set()
	
	search_paths = [
		"/usr/share/applications",
		"/usr/local/share/applications",
		os.path.expanduser("~/.local/share/applications")
	]
	
	for app_dir in search_paths:
		if not os.path.exists(app_dir):
			continue
	
		for file_path in glob.glob(os.path.join(app_dir, "*.desktop")):
			try:
				with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
					content = f.read()
	
				if "WebBrowser" not in content:
					continue
	
				name = None
				exec_cmd = None
	
				for line in content.splitlines():
					if line.startswith("Name=") and not name:
						name = line.split("=", 1)[1].strip()
	
					if line.startswith("Exec=") and not exec_cmd:
						raw_cmd = line.split("=", 1)[1].strip()
						parts = raw_cmd.split()
	
						if parts:
							exec_cmd = parts[0].strip('"')
	
				if name and exec_cmd:
					result = _get_browser_from_binary(
							browser_name=name,
							binary_name=exec_cmd,
							processed_paths=processed_paths
					)
	
					if result is None:
						continue
	
					found_browser, path_obj = result
	
					found_browsers.append(found_browser)
					processed_paths.add(path_obj)
			except (Exception,):
				continue
				
	for name, binaries in _STANDARD_BROWSERS_BINARIES.items():
		for binary in binaries:
			result = _get_browser_from_binary(browser_name=name, binary_name=binary, processed_paths=processed_paths)
	
			if result is None:
				continue
	
			found_browser, path_obj = result
	
			found_browsers.append(found_browser)
			processed_paths.add(path_obj)
	
	return found_browsers


_STANDARD_BROWSERS_BINARIES = {
	"Google Chrome": [
		"google-chrome",
		"google-chrome-stable",
		"google-chrome-beta",
		"google-chrome-unstable",
		"chrome"
	],
	"Chromium": ["chromium", "chromium-browser", "chromium-freeworld"],
	"Microsoft Edge": [
		"microsoft-edge",
		"microsoft-edge-stable",
		"microsoft-edge-beta",
		"microsoft-edge-dev",
		"microsoft-edge-canary"
	],
	"Yandex": ["yandex-browser", "yandex-browser-beta", "yandex_browser"]
}
