import re
import psutil
from typing import Iterator, Optional
from osn_selenium._functions import validate_path
from osn_selenium._typehints import PATH_TYPEHINT
from osn_system_utils.api._utils import LOCALHOST_IPS
from osn_selenium.webdrivers._executable_tables.models import ExecutablesTableRow


__all__ = [
	"find_browser_previous_session",
	"get_active_executables_table",
	"get_found_profile_dir"
]


def get_found_profile_dir(row: ExecutablesTableRow, profile_dir_command: str) -> Optional[str]:
	"""
	Extracts the profile directory path from the command line of a running process.

	Args:
		row (ExecutablesTableRow): The data row containing the PID of the process.
		profile_dir_command (str): The command line pattern to search for, using `{value}` as placeholder.

	Returns:
		Optional[str]: The extracted profile directory path if found, otherwise None.
	"""
	
	try:
		proc = psutil.Process(row.pid)
		cmdline_args = proc.cmdline()
	
		found_command_line = " ".join(cmdline_args)
		pattern = profile_dir_command.format(value="(.*?)")
	
		found_profile_dir = re.search(pattern=pattern, string=found_command_line)
	
		if found_profile_dir is not None:
			result = found_profile_dir.group(1)
	
			return result
	except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
		return None
	
	return None


def get_active_executables_table(browser_exe: PATH_TYPEHINT) -> Iterator[ExecutablesTableRow]:
	"""
	Iterates through active network connections to find processes matching the browser executable.

	Args:
		browser_exe (PATH_TYPEHINT): Path or name of the browser executable.

	Returns:
		Iterator[ExecutablesTableRow]: An iterator of matching process information rows.
	"""
	
	target_name = validate_path(path=browser_exe).name
	
	for conn in psutil.net_connections(kind="inet"):
		if (
				conn.status != psutil.CONN_LISTEN
				or not conn.laddr
				or conn.laddr.ip not in LOCALHOST_IPS
				or not conn.pid
		):
			continue
	
		try:
			process = psutil.Process(conn.pid)
			process_name = process.name()
	
			if process_name.lower() == target_name.lower():
				yield ExecutablesTableRow(
						executable=process_name,
						address=f"{conn.laddr.ip}:{conn.laddr.port}",
						pid=conn.pid,
				)
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			continue


def find_browser_previous_session(
		browser_exe: PATH_TYPEHINT,
		profile_dir_command: str,
		profile_dir: Optional[str]
) -> Optional[int]:
	"""
	Finds the port number of a previously opened browser session, if it exists.

	This function checks for an existing browser session by examining network connections.
	It searches for listening connections associated with the given browser executable and profile directory.

	Args:
		browser_exe (PATH_TYPEHINT): Path to the browser executable or just the executable name.
		profile_dir_command (str): Command line pattern to find the profile directory argument.
								   Should use `{value}` as a placeholder for the directory path.
		profile_dir (Optional[str]): The expected profile directory path to match against.

	Returns:
		Optional[int]: The port number of the previous session if found and matched, otherwise None.
	"""
	
	ip_pattern = re.compile(r"127\.0\.0\.1:(\d+)")
	
	for row in get_active_executables_table(browser_exe=browser_exe):
		found_profile_dir = get_found_profile_dir(row=row, profile_dir_command=profile_dir_command)
	
		if found_profile_dir == profile_dir:
			return int(re.search(pattern=ip_pattern, string=row.address).group(1))
	
	return None
