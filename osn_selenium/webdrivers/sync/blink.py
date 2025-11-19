import re
import sys
import pathlib
import warnings
from subprocess import Popen
from selenium import webdriver
from osn_selenium.types import WindowRect
from osn_selenium.flags.base import ArgumentValue
from osn_selenium.flags.blink import BlinkFlagsManager
from osn_selenium.webdrivers.sync.base import WebDriver
from osn_selenium.trio_base_mixin import requires_driver
from osn_selenium.browsers_handler import get_path_to_browser
from osn_windows_cmd.taskkill.parameters import TaskKillTypes
from osn_windows_cmd.taskkill import (
	ProcessID,
	taskkill_windows
)
from typing import (
	Any,
	Mapping,
	Optional,
	Sequence,
	Type,
	Union
)
from osn_selenium.abstract.webdriver.blink import (
	AbstractBlinkWebDriver
)
from osn_selenium.webdrivers._functions import (
	find_browser_previous_session
)
from osn_selenium.flags.utils.blink import (
	BlinkArguments,
	BlinkExperimentalOptions,
	BlinkFlags
)
from osn_windows_cmd.netstat import (
	get_localhost_minimum_free_port,
	get_localhost_pids_with_addresses,
	get_localhost_pids_with_ports
)


class BlinkWebDriver(WebDriver, AbstractBlinkWebDriver):
	def __init__(
			self,
			browser_exe: Optional[Union[str, pathlib.Path]],
			browser_name_in_system: str,
			webdriver_path: str,
			use_browser_exe: bool = True,
			flags_manager_type: Type[BlinkFlagsManager] = BlinkFlagsManager,
			flags: Optional[BlinkFlags] = None,
			start_page_url: str = "",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
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
			flags (Optional[BlinkFlags]): Initial browser flags or options
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
		)
		
		self.update_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url
		)
	
	@requires_driver
	def delete_network_conditions(self) -> None:
		self.driver.delete_network_conditions()
	
	@requires_driver
	def get_issue_message(self) -> Any:
		return self.driver.get_issue_message()
	
	@requires_driver
	def get_log(self, log_type: str) -> Any:
		return self.driver.get_log(log_type=log_type)
	
	@requires_driver
	def get_network_conditions(self) -> Mapping[str, Any]:
		return self.driver.get_network_conditions()
	
	@requires_driver
	def get_sinks(self) -> Sequence:
		return self.driver.get_sinks()
	
	@requires_driver
	def launch_app(self, id: str) -> Mapping[str, Any]:
		return self.driver.launch_app(id=id)
	
	@property
	@requires_driver
	def log_types(self) -> Any:
		return self.driver.log_types
	
	@property
	def debugging_port(self) -> Optional[int]:
		return self._webdriver_flags_manager.arguments.get("remote_debugging_port", ArgumentValue(command_line="", value=None)).value
	
	@property
	def browser_exe(self) -> Optional[Union[str, pathlib.Path]]:
		return self._webdriver_flags_manager.browser_exe
	
	def _find_debugging_port(self, debugging_port: Optional[int]) -> int:
		if self.browser_exe is not None:
			user_data_dir_command = self._webdriver_flags_manager.flags_definitions.get("user_data_dir", None)
			user_data_dir_value = self._webdriver_flags_manager.arguments.get("user_data_dir", None)
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
		return self._webdriver_flags_manager.arguments.get("remote_debugging_address", {}).get("value", None)
	
	def _detect_browser_exe(self, browser_name_in_system: str, use_browser_exe: bool):
		if self.browser_exe is None and use_browser_exe:
			self._webdriver_flags_manager.browser_exe = get_path_to_browser(browser_name_in_system)
		elif self.browser_exe is not None and not use_browser_exe:
			self._webdriver_flags_manager.browser_exe = None
	
	def set_start_page_url(self, start_page_url: str):
		self._webdriver_flags_manager.start_page_url = start_page_url
	
	def reset_settings(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	):
		if not self.is_active:
			if window_rect is None:
				window_rect = WindowRect()
		
			if flags is not None:
				self._webdriver_flags_manager.set_flags(flags)
			else:
				self._webdriver_flags_manager.clear_flags()
		
			self._webdriver_flags_manager.browser_exe = browser_exe
		
			self.set_start_page_url(start_page_url)
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
		raise NotImplementedError("This function must be implemented in child classes.")
	
	def _check_browser_exe_active(self) -> bool:
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
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		if flags is not None:
			self._webdriver_flags_manager.update_flags(flags)
		
		if browser_exe is not None:
			self._webdriver_flags_manager.browser_exe = browser_exe
		
		if start_page_url is not None:
			self.set_start_page_url(start_page_url)
		
		if window_rect is not None:
			self._window_rect = window_rect
		
		if use_browser_exe is not None and browser_name_in_system is not None:
			self._detect_browser_exe(
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe
			)
		
		self._set_debugging_port(self._find_debugging_port(self.debugging_port), self.debugging_ip)
	
	@property
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge]]:
		return super().driver
	
	def start_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		if self.driver is None:
			self.update_settings(
					flags=flags,
					browser_exe=browser_exe,
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
					start_page_url=start_page_url,
					window_rect=window_rect,
			)
		
			if self.browser_exe is not None:
				self._is_active = self._check_browser_exe_active()
		
				if not self._is_active:
					Popen(args=self._webdriver_flags_manager.start_command, shell=True)
		
					while not self._is_active:
						self._is_active = self._check_browser_exe_active()
		
			self._create_driver()
	
	def close_webdriver(self):
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
		
		if self.driver is not None:
			self.driver.quit()
			self._driver = None
	
	def restart_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		self.close_webdriver()
		self.start_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
		)
	
	@requires_driver
	def set_network_conditions(self, **network_conditions: Mapping[str, Any]) -> None:
		self.driver.set_network_conditions(**network_conditions)
	
	@requires_driver
	def set_permissions(self, name: str, value: str) -> None:
		self.driver.set_permissions(name=name, value=value)
	
	@requires_driver
	def set_sink_to_use(self, sink_name: str) -> Mapping:
		return self.driver.set_sink_to_use(sink_name=sink_name)
	
	@requires_driver
	def start_desktop_mirroring(self, sink_name: str) -> Mapping[str, Any]:
		return self.driver.start_desktop_mirroring(sink_name=sink_name)
	
	@requires_driver
	def start_tab_mirroring(self, sink_name: str) -> Mapping[str, Any]:
		return self.driver.start_tab_mirroring(sink_name=sink_name)
	
	@requires_driver
	def stop_casting(self, sink_name: str) -> Mapping[str, Any]:
		return self.driver.stop_casting(sink_name=sink_name)
