import re
import sys
import pathlib
from subprocess import PIPE, Popen
from typing import Optional, Union
from pandas import DataFrame, Series
from osn_selenium.errors import (
	PlatformNotSupportedError
)
from osn_windows_cmd.netstat import (
	get_netstat_connections_data as windows_netstat_connections_data
)


def get_found_profile_dir(data: Series, profile_dir_command: str) -> Optional[str]:
	"""
	Extracts the browser profile directory path from a process's command line arguments.

	This function executes a platform-specific command to retrieve the command line
	of a process given its PID. It then searches for a profile directory path within
	the command line using a provided command pattern. Currently, only Windows platform is supported.

	Args:
		data (Series): A Pandas Series containing process information, which must include a 'PID' column
			representing the process ID.
		profile_dir_command (str): A string representing the command line pattern to search for the profile directory.
			This string should contain '{value}' as a placeholder where the profile directory path is expected.
			For example: "--user-data-dir='{value}'".

	Returns:
		Optional[str]: The profile directory path as a string if found in the command line, otherwise None.

	Raises:
		PlatformNotSupportedError: If the platform is not supported.
	"""
	
	if sys.platform == "win32":
		stdout = Popen(
				f"wmic process where processid={int(data['PID'])} get CommandLine /FORMAT:LIST",
				stdout=PIPE,
				shell=True
		).communicate()[0].decode("866", errors="ignore").strip()
		found_command_line = re.sub(r"^CommandLine=", "", stdout).strip()
	
		found_profile_dir = re.search(profile_dir_command.format(value="(.*?)"), found_command_line)
		if found_profile_dir is not None:
			found_profile_dir = found_profile_dir.group(1)
	
		return found_profile_dir
	
	raise PlatformNotSupportedError(f"Unsupported platform: {sys.platform}.")


def get_active_executables_table(browser_exe: Union[str, pathlib.Path]) -> DataFrame:
	"""
	Retrieves a table of active executables related to a specified browser, listening on localhost.

	This function uses platform-specific methods to fetch network connection information
	and filters it to find entries associated with the provided browser executable
	that are in a "LISTENING" state on localhost. Currently, only Windows platform is supported.

	Args:
		browser_exe (Union[str, pathlib.Path]): The path to the browser executable.
			It can be a string or a pathlib.Path object.

	Returns:
		DataFrame: A Pandas DataFrame containing rows of active executable connections
			that match the browser executable and listening criteria.
			Returns an empty DataFrame if no matching executables are found.

	Raises:
		PlatformNotSupportedError: If the platform is not supported.
	"""
	
	if sys.platform == "win32":
		connections_data = windows_netstat_connections_data(
				show_all_ports=True,
				show_connections_exe=True,
				show_connection_pid=True
		)
	
		return connections_data.loc[
			(
					connections_data["Executable"] == (browser_exe if isinstance(browser_exe, str) else browser_exe.name)
			) &
			connections_data["Local Address"].str.contains(r"127\.0\.0\.1:\d+", regex=True, na=False) &
			(connections_data["State"] == "LISTENING")
		]
	
	raise PlatformNotSupportedError(f"Unsupported platform: {sys.platform}.")


def find_browser_previous_session(
		browser_exe: Union[str, pathlib.Path],
		profile_dir_command: str,
		profile_dir: Optional[str]
) -> Optional[int]:
	"""
	Finds the port number of a previously opened browser session, if it exists.

	This function checks for an existing browser session by examining network connections.
	It searches for listening connections associated with the given browser executable and profile directory.

	Args:
		browser_exe (Union[str, pathlib.Path]): Path to the browser executable or just the executable name.
		profile_dir_command (str): Command line pattern to find the profile directory argument in the process command line. Should use `{value}` as a placeholder for the directory path.
		profile_dir (Optional[str]): The expected profile directory path to match against.

	Returns:
		Optional[int]: The port number of the previous session if found and matched, otherwise None.
	"""
	
	executables_table = get_active_executables_table(browser_exe)
	
	for index, row in executables_table.iterrows():
		found_profile_dir = get_found_profile_dir(row, profile_dir_command)
	
		if found_profile_dir == profile_dir:
			return int(re.search(r"127\.0\.0\.1:(\d+)", row["Local Address"]).group(1))
	
	return None


def build_cdp_kwargs(**kwargs):
	dict_ = {}
	
	for key, value in kwargs.items():
		if value is not None:
			dict_[key] = value
	
	return dict_
