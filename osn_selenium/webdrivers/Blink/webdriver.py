import re
import sys
import trio
import pathlib
import warnings
from subprocess import Popen
from selenium import webdriver
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union,
	cast
)
from osn_selenium.webdrivers.types import _any_flags_mapping
from osn_selenium.browsers_handler import get_path_to_browser
from osn_windows_cmd.taskkill.parameters import TaskKillTypes
from osn_selenium.captcha_workers import (
	CaptchaWorkerSettings
)
from osn_windows_cmd.taskkill import (
	ProcessID,
	taskkill_windows
)
from osn_selenium.dev_tools.manager import (
	DevTools,
	DevToolsSettings
)
from osn_selenium.webdrivers._functions import (
	find_browser_previous_session
)
from osn_selenium.webdrivers.Blink.protocols import (
	TrioBlinkWebDriverWrapperProtocol
)
from osn_selenium.webdrivers.BaseDriver.webdriver import (
	BrowserWebDriver,
	TrioBrowserWebDriverWrapper
)
from osn_selenium.webdrivers.Blink.flags import (
	BlinkArguments,
	BlinkExperimentalOptions,
	BlinkFlags,
	BlinkFlagsManager
)
from osn_windows_cmd.netstat import (
	get_localhost_minimum_free_port,
	get_localhost_pids_with_addresses,
	get_localhost_pids_with_ports
)


class BlinkWebDriver(BrowserWebDriver):
	"""
	A WebDriver manager for Blink-based browsers (e.g., Chrome, Edge).

	Extends `BrowserWebDriver` with functionality specific to Blink-based browsers,
	such as managing the browser executable, handling remote debugging ports, and finding
	pre-existing browser sessions.

	Attributes:
		_window_rect (Optional[WindowRect]): The window size and position settings.
		_js_scripts (dict[str, str]): A dictionary of pre-loaded JavaScript scripts.
		_webdriver_path (str): The file path to the WebDriver executable.
		_webdriver_flags_manager (BlinkFlagsManager): The manager for browser flags and options.
		_driver (Optional[Union[webdriver.Chrome, webdriver.Edge]]): The active Selenium WebDriver instance.
		_base_implicitly_wait (int): The default implicit wait time in seconds.
		_base_page_load_timeout (int): The default page load timeout in seconds.
		_base_script_timeout (int): The default script timeout in seconds.
		_captcha_workers (Sequence[CaptchaWorkerSettings]): A list of configured captcha worker settings.
		_is_active (bool): A flag indicating if the browser process is active.
		trio_capacity_limiter (trio.CapacityLimiter): A capacity limiter for controlling concurrent async operations.
		dev_tools (DevTools): An interface for interacting with the browser's DevTools protocol.
		_console_encoding (str): The encoding of the system console.
		_ip_pattern (re.Pattern): A compiled regex pattern to match IP addresses and ports.
	"""
	
	def __init__(
			self,
			browser_exe: Optional[Union[str, pathlib.Path]],
			browser_name_in_system: str,
			webdriver_path: str,
			use_browser_exe: bool = True,
			flags_manager_type: Type[BlinkFlagsManager] = BlinkFlagsManager,
			flags: Optional[Union[BlinkFlags, _any_flags_mapping]] = None,
			start_page_url: str = "",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Union[int, float] = 40,
			captcha_workers: Optional[list[CaptchaWorkerSettings]] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
	):
		"""
		Initializes the BlinkWebDriver instance.

		This constructor sets up the necessary components for controlling a Blink-based browser,
		including paths, flag managers, timeouts, and integration with DevTools and Trio.
		It also initializes properties related to console encoding and IP pattern matching
		for managing browser processes.

		Args:
			browser_exe (Optional[Union[str, pathlib.Path]]): The path to the browser executable
				(e.g., `chrome.exe` or `msedge.exe`). If None, the browser executable will not be
				managed directly by this class (e.g., for remote WebDriver connections where the
				browser is already running).
			browser_name_in_system (str): The common name of the browser executable in the system
				(e.g., "Chrome", "Edge"). Used to auto-detect `browser_exe` if `use_browser_exe` is True.
			webdriver_path (str): The file path to the WebDriver executable (e.g., `chromedriver.exe`).
			use_browser_exe (bool): If True, the browser executable path will be
				automatically determined based on `browser_name_in_system` if `browser_exe`
				is not explicitly provided. If False, `browser_exe` must be None.
				Defaults to True.
			flags_manager_type (Type[BlinkFlagsManager]): The type of flags manager to use.
				Defaults to `BlinkFlagsManager`, which is suitable for Chrome/Edge.
			flags (Optional[Union[BlinkFlags, Mapping[str, Any]]]): Initial browser flags or options
				specific to Blink-based browsers. Can be a `BlinkFlags` object or a generic mapping.
				Defaults to None.
			start_page_url (str): The URL that the browser will attempt to navigate to
				immediately after starting. Defaults to an empty string.
			implicitly_wait (int): The default implicit wait time in seconds for element searches.
				Defaults to 5.
			page_load_timeout (int): The default page load timeout in seconds. Defaults to 5.
			script_timeout (int): The default asynchronous script timeout in seconds. Defaults to 5.
			window_rect (Optional[WindowRect]): The initial window size and position. If None,
				the browser's default window size will be used. Defaults to None.
			trio_tokens_limit (Union[int, float]): The maximum number of concurrent synchronous
				WebDriver operations allowed when using the Trio wrapper. Defaults to 40.
			captcha_workers (Optional[Sequence[CaptchaWorkerSettings]]): A sequence of
				settings for captcha detection and solving functions.
				Defaults to None, which results in an empty list.
			devtools_settings (Optional[DevToolsSettings]): Settings for configuring the
				Chrome DevTools Protocol (CDP) interface. Defaults to None.
		"""
		
		self._console_encoding = sys.stdout.encoding
		self._ip_pattern = re.compile(r"\A(\d+\.\d+\.\d+\.\d+|\[::]):\d+\Z")
		
		super().__init__(
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
				captcha_workers=captcha_workers,
				devtools_settings=devtools_settings,
		)
		
		self.update_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url
		)
	
	@property
	def debugging_port(self) -> Optional[int]:
		"""
		Gets the currently set debugging port.

		Retrieves the debugging port number that the browser instance is configured to use.

		Returns:
			Optional[int]: The debugging port number, or None if not set.
		"""
		
		return self._webdriver_flags_manager._arguments.get("remote_debugging_port", {}).get("value", None)
	
	@property
	def browser_exe(self) -> Optional[Union[str, pathlib.Path]]:
		"""
		Gets the path to the browser executable.

		Returns:
			Optional[Union[str, pathlib.Path]]: The path to the browser executable.
		"""
		
		return self._webdriver_flags_manager.browser_exe
	
	def _find_debugging_port(self, debugging_port: Optional[int]) -> int:
		"""
		Finds an appropriate debugging port, either reusing a previous session's port or finding a free port.

		Attempts to locate a suitable debugging port for the browser. It first tries to reuse a debugging port
		from a previous browser session if a profile directory is specified and a previous session is found.
		If no previous session is found or if no profile directory is specified, it attempts to use the provided
		`debugging_port` if available, or finds a minimum free port if no port is provided or the provided port is in use.

		Args:
			debugging_port (Optional[int]): Requested debugging port number. If provided, the method attempts to use this port. Defaults to None.

		Returns:
			int: The debugging port number to use. This is either a reused port from a previous session, the provided port if available, or a newly found free port.
		"""
		
		if self.browser_exe is not None:
			user_data_dir_command = self._webdriver_flags_manager._flags_definitions.get("user_data_dir", None)
			user_data_dir_value = self._webdriver_flags_manager._arguments.get("user_data_dir", None)
			user_data_dir = None if user_data_dir_command is None else user_data_dir_value["value"]
		
			if user_data_dir_command is not None:
				previous_session = find_browser_previous_session(self.browser_exe, user_data_dir_command["command"], user_data_dir)
		
				if previous_session is not None:
					return previous_session
		
		if debugging_port is not None:
			return get_localhost_minimum_free_port(
					console_encoding=self._console_encoding,
					ip_pattern=self._ip_pattern,
					ports_to_check=debugging_port
			)
		
		if self.debugging_port is None or self.debugging_port == 0:
			return get_localhost_minimum_free_port(
					console_encoding=self._console_encoding,
					ip_pattern=self._ip_pattern,
					ports_to_check=self.debugging_port
			)
		
		return self.debugging_port
	
	def _set_debugging_port(self, debugging_port: Optional[int], debugging_address: Optional[str]):
		"""
		Sets the debugging port and address.

		Configures the browser to start with a specific debugging port. This port is used for external tools,
		like debuggers or browser automation frameworks, to connect to and control the browser instance.
		Setting a fixed debugging port can be useful for consistent remote debugging or automation setups.

		Args:
			debugging_port (Optional[int]): Debugging port number. If None or 0, the browser chooses a port automatically.
			debugging_address (Optional[str]): The IP address for the debugger to listen on. Defaults to '127.0.0.1'.
		"""
		
		if self.browser_exe is not None:
			_debugging_address = "127.0.0.1" if debugging_address is None else debugging_address
			_debugging_port = 0 if debugging_port is None else debugging_port
		
			self._webdriver_flags_manager.update_flags(
					BlinkFlags(
							argument=BlinkArguments(
									remote_debugging_port=debugging_port,
									remote_debugging_address=debugging_address
							),
							experimental_option=BlinkExperimentalOptions(debugger_address=f"{_debugging_address}:{_debugging_port}"),
					)
			)
	
	@property
	def debugging_ip(self) -> Optional[str]:
		"""
		Gets the IP address part of the debugger address.

		Returns:
			Optional[str]: The IP address of the debugger, or None if not set.
		"""
		
		return self._webdriver_flags_manager._arguments.get("remote_debugging_address", {}).get("value", None)
	
	def _detect_browser_exe(self, browser_name_in_system: str, use_browser_exe: bool):
		"""
		Detects and sets the browser executable path within the flags manager.

		This internal method is responsible for determining the correct path to the
		browser executable based on the `use_browser_exe` flag and the system's
		known browser locations. If `use_browser_exe` is True and no explicit path
		is set, it attempts to find the browser. If `use_browser_exe` is False,
		it ensures the browser executable path is cleared.

		Args:
			browser_name_in_system (str): The common name of the browser (e.g., "Chrome", "Edge")
				used to find its executable on the system.
			use_browser_exe (bool): If True, the method will attempt to find and set
				the browser executable path if it's not already set. If False,
				it will ensure the browser executable path is cleared.
		"""
		
		if self.browser_exe is None and use_browser_exe:
			self._webdriver_flags_manager.browser_exe = get_path_to_browser(browser_name_in_system)
		elif self.browser_exe is not None and not use_browser_exe:
			self._webdriver_flags_manager.browser_exe = None
	
	def set_start_page_url(self, start_page_url: str):
		"""
		Sets the URL that the browser will open upon starting.

		Args:
			start_page_url (str): The URL to set as the start page.
		"""
		
		self._webdriver_flags_manager.start_page_url = start_page_url
	
	def reset_settings(
			self,
			flags: Optional[Union[BlinkFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Union[int, float] = 40,
	):
		"""
		Resets various configurable browser settings to their specified or default values.

		This method allows for reconfiguring the WebDriver's operational parameters,
		such as browser flags, executable path, start URL, window dimensions, and
		concurrency limits. It is crucial that the browser session is *not* active
		when this method is called; otherwise, a warning will be issued, and no changes
		will be applied.

		Args:
			flags (Optional[Union[BlinkFlags, Mapping[str, Any]]]): New browser flags to apply.
				If provided, existing flags are cleared and replaced with these.
				If `None`, all custom flags are cleared, and the browser will start with default flags.
			browser_exe (Optional[Union[str, pathlib.Path]]): The explicit path to the browser executable.
				If provided, this path will be used. If `None`, the executable path managed by the
				flags manager will be cleared, and then potentially re-detected based on
				`use_browser_exe` and `browser_name_in_system`.
			browser_name_in_system (Optional[str]): The common name of the browser (e.g., "Chrome", "Edge").
				Used in conjunction with `use_browser_exe` to automatically detect the browser executable path.
				This parameter only takes effect if `use_browser_exe` is explicitly `True` or `False`.
				If `None`, no automatic detection based on name will occur through this method call.
			use_browser_exe (Optional[bool]): Controls the automatic detection of the browser executable.
				If `True` (and `browser_name_in_system` is provided), the browser executable path
				will be automatically detected if `browser_exe` is `None`.
				If `False` (and `browser_name_in_system` is provided), any existing `browser_exe`
				path in the flags manager will be cleared.
				If `None`, the current `use_browser_exe` state is maintained for the `_detect_browser_exe` logic.
			start_page_url (str): The URL that the browser will attempt to navigate to
				immediately after starting. Defaults to an empty string.
			window_rect (Optional[WindowRect]): The initial window size and position settings.
				If `None`, it defaults to a new `WindowRect()` instance, effectively resetting
				to the browser's default window behavior.
			trio_tokens_limit (Union[int, float]): The maximum number of concurrent synchronous
				WebDriver operations allowed by the Trio capacity limiter. Defaults to 40.
		"""
		
		if not self.is_active:
			if window_rect is None:
				window_rect = WindowRect()
		
			if flags is not None:
				self._webdriver_flags_manager.set_flags(flags)
			else:
				self._webdriver_flags_manager.clear_flags()
		
			self._webdriver_flags_manager.browser_exe = browser_exe
		
			self.set_start_page_url(start_page_url)
			self.set_trio_tokens_limit(trio_tokens_limit)
			self._window_rect = window_rect
		
			if use_browser_exe is not None and browser_name_in_system is not None:
				self._detect_browser_exe(
						browser_name_in_system=browser_name_in_system,
						use_browser_exe=use_browser_exe
				)
		
			if self.browser_exe is not None and self.debugging_port is not None or self.debugging_ip is not None:
				self._set_debugging_port(self._find_debugging_port(self.debugging_port), self.debugging_ip)
		else:
			warnings.warn("Browser is already running.")
	
	def _create_driver(self):
		"""
		Abstract method to create a WebDriver instance. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide browser-specific
		WebDriver instantiation logic (e.g., creating ChromeDriver, FirefoxDriver, etc.).

		Raises:
			NotImplementedError: If the method is not implemented in a subclass.
		"""
		
		raise NotImplementedError("This function must be implemented in child classes.")
	
	def _check_browser_exe_active(self) -> bool:
		"""
		Checks if the WebDriver is active by verifying if the debugging port is in use.

		Determines if a WebDriver instance is currently running and active by checking if the configured
		debugging port is in use by any process. This is a way to verify if a browser session is active
		without directly querying the WebDriver itself.

		Returns:
			bool: True if the WebDriver is active (debugging port is in use), False otherwise.
		"""
		
		for pid, ports in get_localhost_pids_with_addresses(console_encoding=self._console_encoding, ip_pattern=self._ip_pattern).items():
			if len(ports) == 1 and re.search(rf":{self.debugging_port}\Z", ports[0]) is not None:
				address = re.search(rf"\A(.+):{self.debugging_port}\Z", ports[0]).group(1)
		
				if address != self.debugging_ip:
					self._set_debugging_port(
							debugging_port=self.debugging_port,
							debugging_address=re.search(rf"\A(.+):{self.debugging_port}\Z", ports[0]).group(1)
					)
		
				return True
		
		return False
	
	def update_settings(
			self,
			flags: Optional[Union[BlinkFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Updates various browser settings selectively without resetting others.

		This method allows for dynamic updating of browser settings. Only the settings
		for which a non-None value is provided will be updated. Settings passed as `None`
		will retain their current values. This method can be called whether the browser
		is active or not, but some changes might only take effect after the browser is
		restarted.

		Args:
			flags (Optional[Union[BlinkFlags, Mapping[str, Any]]]): New browser flags to update.
				If provided, these flags will be merged with or overwrite existing flags
				within the flags manager. If `None`, existing flags remain unchanged.
			browser_exe (Optional[Union[str, pathlib.Path]]): The new path to the browser executable.
				If provided, this path will be set in the flags manager. If `None`, the
				current browser executable path remains unchanged.
			browser_name_in_system (Optional[str]): The common name of the browser (e.g., "Chrome", "Edge").
				Used in conjunction with `use_browser_exe` to automatically detect the browser executable path.
				This parameter only takes effect if `use_browser_exe` is explicitly provided.
				If `None`, no automatic detection based on name will occur through this method call.
			use_browser_exe (Optional[bool]): Controls the automatic detection of the browser executable.
				If `True` (and `browser_name_in_system` is provided), the browser executable path
				will be automatically detected if `browser_exe` is `None`.
				If `False` (and `browser_name_in_system` is provided), any existing `browser_exe`
				path in the flags manager will be cleared.
				If `None`, the current `use_browser_exe` state is maintained for the `_detect_browser_exe` logic.
			start_page_url (Optional[str]): The new URL that the browser will attempt to navigate to
				immediately after starting. If `None`, the current start page URL remains unchanged.
			window_rect (Optional[WindowRect]): The new window size and position settings.
				If `None`, the current window rectangle settings remain unchanged.
			trio_tokens_limit (Optional[Union[int, float]]): The new maximum number of concurrent
				asynchronous operations allowed by the Trio capacity limiter. If `None`, the
				current limit remains unchanged.
		"""
		
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags)
		
		if browser_exe is not None:
			self._webdriver_flags_manager.browser_exe = browser_exe
		
		if start_page_url is not None:
			self.set_start_page_url(start_page_url)
		
		if window_rect is not None:
			self._window_rect = window_rect
		
		if trio_tokens_limit is not None:
			self.set_trio_tokens_limit(trio_tokens_limit)
		
		if use_browser_exe is not None and browser_name_in_system is not None:
			self._detect_browser_exe(
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe
			)
		
		self._set_debugging_port(self._find_debugging_port(self.debugging_port), self.debugging_ip)
	
	@property
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge]]:
		"""
		Gets the underlying Selenium WebDriver instance associated with this object.

		This property provides direct access to the WebDriver object (e.g., Chrome, Edge)
		that is being controlled, allowing for direct Selenium operations if needed.

		Returns:
			Optional[Union[webdriver.Chrome, webdriver.Edge]]:
				The active WebDriver instance, or None if no driver is currently set or active.
		"""
		
		return super().driver
	
	def start_webdriver(
			self,
			flags: Optional[Union[BlinkFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Starts the WebDriver service and the browser session.

		Initializes and starts the WebDriver instance and the associated browser process.
		It first updates settings based on provided parameters (if the driver is not already running),
		checks if a browser process needs to be started, starts it if necessary using Popen,
		waits for it to become active, and then creates the WebDriver client instance (`self.driver`).

		Args:
			flags (Optional[Union[BlinkFlags, Mapping[str, Any]]]): Override flags for this start.
				If provided, these flags will be applied. If `None`, current settings are used.
			browser_exe (Optional[Union[str, pathlib.Path]]): Override browser executable path for this start.
				If provided, this path will be used. If `None`, current settings are used.
			browser_name_in_system (Optional[str]): Override browser name for auto-detection for this start.
				Only takes effect if `use_browser_exe` is also provided. If `None`, current settings are used.
			use_browser_exe (Optional[bool]): Override auto-detection behavior for this start.
				If provided, this boolean determines if the browser executable is auto-detected.
				If `None`, current settings are used.
			start_page_url (Optional[str]): Override start page URL for this start.
				If provided, this URL will be used. If `None`, current setting is used.
			window_rect (Optional[WindowRect]): Override window rectangle for this start.
				If provided, these dimensions will be used. If `None`, current settings are used.
			trio_tokens_limit (Optional[Union[int, float]]): Override Trio token limit for this start.
				If provided, this limit will be used. If `None`, current setting is used.
		"""
		
		if self.driver is None:
			self.update_settings(
					flags=flags,
					browser_exe=browser_exe,
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
					start_page_url=start_page_url,
					window_rect=window_rect,
					trio_tokens_limit=trio_tokens_limit,
			)
		
			if self.browser_exe is not None:
				self._is_active = self._check_browser_exe_active()
		
				if not self._is_active:
					Popen(self._webdriver_flags_manager.start_command, shell=True)
		
					while not self._is_active:
						self._is_active = self._check_browser_exe_active()
		
			self._create_driver()
	
	def close_webdriver(self):
		"""
		Closes the WebDriver instance and terminates the associated browser subprocess.

		Quits the current WebDriver session, closes all browser windows, and then forcefully terminates
		the browser process. This ensures a clean shutdown of the browser and WebDriver environment.
		"""
		
		if self.browser_exe is not None:
			for pid, ports in get_localhost_pids_with_ports(console_encoding=self._console_encoding, ip_pattern=self._ip_pattern).items():
				if ports == [self.debugging_port]:
					taskkill_windows(
							taskkill_type=TaskKillTypes.forcefully_terminate,
							selectors=ProcessID(pid)
					)
		
					self._is_active = self._check_browser_exe_active()
		
					while self._is_active:
						self._is_active = self._check_browser_exe_active()
		
		if self._driver is not None:
			self._driver.quit()
			self._driver = None
	
	def restart_webdriver(
			self,
			flags: Optional[Union[BlinkFlags, _any_flags_mapping]] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
			trio_tokens_limit: Optional[Union[int, float]] = None,
	):
		"""
		Restarts the WebDriver and browser session gracefully.

		Performs a clean restart by first closing the existing WebDriver session and browser
		(using `close_webdriver`), and then initiating a new session (using `start_webdriver`)
		with potentially updated settings. If settings arguments are provided, they override
		the existing settings for the new session; otherwise, the current settings are used.

		Args:
			flags (Optional[Union[BlinkFlags, Mapping[str, Any]]]): Override flags for the new session.
				If provided, these flags will be applied. If `None`, current settings are used.
			browser_exe (Optional[Union[str, pathlib.Path]]): Override browser executable for the new session.
				If provided, this path will be used. If `None`, current settings are used.
			browser_name_in_system (Optional[str]): Override browser name for auto-detection for the new session.
				Only takes effect if `use_browser_exe` is also provided. If `None`, current settings are used.
			use_browser_exe (Optional[bool]): Override auto-detection behavior for the new session.
				If provided, this boolean determines if the browser executable is auto-detected.
				If `None`, current settings are used.
			start_page_url (Optional[str]): Override start page URL for the new session.
				If provided, this URL will be used. If `None`, current setting is used.
			window_rect (Optional[WindowRect]): Override window rectangle for the new session.
				If provided, these dimensions will be used. If `None`, current settings are used.
			trio_tokens_limit (Optional[Union[int, float]]): Override Trio token limit for the new session.
				If provided, this limit will be used. If `None`, current setting is used.
		"""
		
		self.close_webdriver()
		self.start_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
				trio_tokens_limit=trio_tokens_limit,
		)
	
	def to_wrapper(self) -> TrioBlinkWebDriverWrapperProtocol:
		"""
		Creates a TrioBrowserWebDriverWrapper instance for asynchronous operations with Trio.

		Wraps the ...WebDriver instance in a TrioBrowserWebDriverWrapper, which allows for running WebDriver
		commands in a non-blocking manner within a Trio asynchronous context. This is essential for
		integrating Selenium WebDriver with asynchronous frameworks like Trio.

		Returns:
			TrioBlinkWebDriverWrapperProtocol: A TrioBrowserWebDriverWrapper instance wrapping this BrowserWebDriver.
		"""
		
		return cast(
				TrioBlinkWebDriverWrapperProtocol,
				TrioBrowserWebDriverWrapper(_webdriver=self)
		)
