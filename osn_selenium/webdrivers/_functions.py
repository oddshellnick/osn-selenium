import re
import trio
import psutil
import pathlib
from pandas import DataFrame, Series
from osn_system_utils.api._utils import LOCALHOST_IPS
from osn_selenium.instances.errors import ExpectedTypeError
from osn_selenium.instances.protocols import AnyInstanceWrapper
from typing import (
	Any,
	Dict,
	List,
	Optional,
	TYPE_CHECKING,
	Union
)
from osn_selenium.instances.sync.web_element import (
	WebElement as SyncWebElement
)
from selenium.webdriver.remote.webelement import (
	WebElement as SeleniumWebElement
)
from osn_selenium.instances.trio_threads.web_element import (
	WebElement as TrioThreadWebElement
)
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper,
	get_trio_thread_instance_wrapper
)


if TYPE_CHECKING:
	from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin as SyncCoreWebDriver
	from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin as TrioThreadCoreWebDriver


def get_found_profile_dir(data: Series, profile_dir_command: str) -> Optional[str]:
	"""
	Extracts the browser profile directory path from a process's command line arguments.

	Args:
		data (Series): A Pandas Series containing process information, which must include a 'PID' column.
		profile_dir_command (str): A string representing the command line pattern.
								   Example: "--user-data-dir='{value}'" or "--user-data-dir={value}"

	Returns:
		Optional[str]: The profile directory path if found, otherwise None.
	"""
	
	pid = int(data["PID"])
	
	try:
		proc = psutil.Process(pid)
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


def get_active_executables_table(browser_exe: Union[str, pathlib.Path]) -> DataFrame:
	"""
	Retrieves a table of active executables related to a specified browser, listening on localhost.

	This function uses platform-specific methods to fetch network connection information
	and filters it to find entries associated with the provided browser executable
	that are in a "LISTENING" state on localhost.

	Args:
		browser_exe (Union[str, pathlib.Path]): The path to the browser executable.
											   It can be a string or a pathlib.Path object.

	Returns:
		DataFrame: A Pandas DataFrame containing rows of active executable connections
				   that match the browser executable and listening criteria.
				   Returns an empty DataFrame if no matching executables are found.
	"""
	
	target_name = browser_exe if isinstance(browser_exe, str) else browser_exe.name
	rows: List[Dict[str, Union[str, int]]] = []
	
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
				rows.append(
						{
							"Executable": process_name,
							"Local Address": f"{conn.laddr.ip}:{conn.laddr.port}",
							"PID": conn.pid
						}
				)
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			continue
	
	return DataFrame(rows)


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
		profile_dir_command (str): Command line pattern to find the profile directory argument.
								   Should use `{value}` as a placeholder for the directory path.
		profile_dir (Optional[str]): The expected profile directory path to match against.

	Returns:
		Optional[int]: The port number of the previous session if found and matched, otherwise None.
	"""
	
	executables_table = get_active_executables_table(browser_exe)
	ip_pattern = re.compile(r"127\.0\.0\.1:(\d+)")
	
	for index, row in executables_table.iterrows():
		found_profile_dir = get_found_profile_dir(row, profile_dir_command)
	
		if found_profile_dir == profile_dir:
			return int(re.search(pattern=ip_pattern, string=row["Local Address"]).group(1))
	
	return None


def wrap_trio_thread_args(args: Any, lock: trio.Lock, limiter: trio.CapacityLimiter) -> Any:
	"""
	Recursively wraps Selenium WebElements into TrioThreadWebElement instances.

	Args:
		args (Any): Data structure containing potential Selenium WebElements.
		lock (trio.Lock): Trio lock for synchronization.
		limiter (trio.CapacityLimiter): Trio capacity limiter.

	Returns:
		Any: Data structure with wrapped elements.
	"""
	
	if isinstance(args, list):
		return [wrap_trio_thread_args(arg, lock=lock, limiter=limiter) for arg in args]
	
	if isinstance(args, set):
		return {wrap_trio_thread_args(arg, lock=lock, limiter=limiter) for arg in args}
	
	if isinstance(args, tuple):
		return (wrap_trio_thread_args(arg, lock=lock, limiter=limiter) for arg in args)
	
	if isinstance(args, dict):
		return {
			wrap_trio_thread_args(key, lock=lock, limiter=limiter): wrap_trio_thread_args(value, lock=lock, limiter=limiter)
			for key, value in args.items()
		}
	
	if isinstance(args, SeleniumWebElement):
		return get_trio_thread_instance_wrapper(
				wrapper_class=TrioThreadWebElement,
				legacy_object=args,
				lock=lock,
				limiter=limiter,
		)
	
	return args


def wrap_sync_args(args: Any) -> Any:
	"""
	Recursively wraps Selenium WebElements into SyncWebElement instances.

	Args:
		args (Any): Data structure containing potential Selenium WebElements.

	Returns:
		Any: Data structure with wrapped elements.
	"""
	
	if isinstance(args, list):
		return [wrap_sync_args(arg) for arg in args]
	
	if isinstance(args, set):
		return {wrap_sync_args(arg) for arg in args}
	
	if isinstance(args, tuple):
		return (wrap_sync_args(arg) for arg in args)
	
	if isinstance(args, dict):
		return {wrap_sync_args(key): wrap_sync_args(value) for key, value in args.items()}
	
	if isinstance(args, SeleniumWebElement):
		return get_sync_instance_wrapper(wrapper_class=SyncWebElement, legacy_object=args)
	
	return args


def wrap_args(driver: Union["SyncCoreWebDriver", "TrioThreadCoreWebDriver"], args: Any) -> Any:
	"""
	Wraps arguments based on the type of the provided driver.

	Args:
		driver (Union[SyncCoreWebDriver, TrioThreadCoreWebDriver]): The driver instance.
		args (Any): Data structure to wrap.

	Returns:
		Any: Wrapped data structure.

	Raises:
		ExpectedTypeError: If the driver is not a recognized type.
	"""
	
	from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin as SyncCoreWebDriver
	if isinstance(driver, SyncCoreWebDriver):
		return wrap_sync_args(args)
	
	from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin as TrioThreadCoreWebDriver
	if isinstance(driver, TrioThreadCoreWebDriver):
		return wrap_trio_thread_args(args, lock=driver._lock, limiter=driver._capacity_limiter)
	
	raise ExpectedTypeError(
			expected_class=(SyncCoreWebDriver, TrioThreadCoreWebDriver),
			received_instance=driver
	)


def unwrap_args(args: Any) -> Any:
	"""
	Recursively unwraps objects by extracting the legacy Selenium object from wrappers.

	Args:
		args (Any): Data structure containing potential instance wrappers.

	Returns:
		Any: Data structure with raw Selenium objects.
	"""
	
	if isinstance(args, list):
		return [unwrap_args(arg) for arg in args]
	
	if isinstance(args, set):
		return {unwrap_args(arg) for arg in args}
	
	if isinstance(args, tuple):
		return (unwrap_args(arg) for arg in args)
	
	if isinstance(args, dict):
		return {unwrap_args(key): unwrap_args(value) for key, value in args.items()}
	
	if isinstance(args, AnyInstanceWrapper):
		return args.legacy
	
	return args


def execute_js_bridge(
		driver: Union["SyncCoreWebDriver", "TrioThreadCoreWebDriver"],
		script: str,
		*args: Any
) -> Any:
	"""
	Executes a JavaScript script via the driver, handling wrapper conversion.

	Args:
		driver (Union[SyncCoreWebDriver, TrioThreadCoreWebDriver]): The driver instance.
		script (str): JavaScript code.
		*args (Any): Script arguments.

	Returns:
		Any: The result of the script execution, wrapped if necessary.
	"""
	
	args = unwrap_args(args)
	
	result = driver.driver.execute_script(script, *args)
	
	return wrap_args(driver=driver, args=result)


def execute_cmd_bridge(
		driver: Union["SyncCoreWebDriver", "TrioThreadCoreWebDriver"],
		cmd: str,
		cmd_args: Dict[str, Any]
) -> Any:
	"""
	Executes a CDP command via the driver, handling wrapper conversion.

	Args:
		driver (Union[SyncCoreWebDriver, TrioThreadCoreWebDriver]): The driver instance.
		cmd (str): CDP command name.
		cmd_args (Mapping[str, Any]): Command arguments.

	Returns:
		Any: The result of the command, wrapped if necessary.
	"""
	
	cmd_args = unwrap_args(cmd_args)
	
	result = driver.driver.execute_cdp_cmd(cmd, cmd_args)
	
	return wrap_args(driver=driver, args=result)


def build_cdp_kwargs(**kwargs: Any) -> Dict[str, Any]:
	"""
	Builds a dictionary of keyword arguments for a CDP command, excluding None values.

	Args:
		**kwargs (Any): Keyword arguments to filter.

	Returns:
		Dict[str, Any]: A dictionary containing only the non-None keyword arguments.
	"""
	
	dict_ = {}
	
	for key, value in kwargs.items():
		if value is not None:
			dict_[key] = value
	
	return dict_
