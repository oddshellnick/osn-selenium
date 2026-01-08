import re
import sys
import trio
import pathlib
from selenium import webdriver
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.blink import BlinkFlagsManager
from osn_selenium.flags.models.values import ArgumentValue
from osn_selenium.browsers_handler import get_path_to_browser
from osn_selenium.webdrivers.trio_threads.base.base import BaseMixin
from osn_windows_cmd.netstat import (
	get_localhost_minimum_free_port
)
from osn_selenium.webdrivers._functions import (
	find_browser_previous_session
)
from osn_selenium.abstract.webdriver.blink.base import (
	AbstractBlinkBaseMixin
)
from osn_selenium.flags.models.blink import (
	BlinkArguments,
	BlinkExperimentalOptions,
	BlinkFlags
)


class BlinkBaseMixin(BaseMixin, AbstractBlinkBaseMixin):
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
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
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
			capacity_limiter (Optional[trio.CapacityLimiter]): A Trio capacity limiter used to
				throttle concurrent thread-based operations. Defaults to None.
		"""
		
		super().__init__(
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				capacity_limiter=capacity_limiter,
		)
		
		self._console_encoding = sys.stdout.encoding
		self._ip_pattern = re.compile(r"\A(\d+\.\d+\.\d+\.\d+|\[::]):\d+\Z")
		
		if browser_exe is not None:
			self._webdriver_flags_manager.browser_exe = browser_exe
		
		if start_page_url is not None:
			self._webdriver_flags_manager.start_page_url = start_page_url
		
		if window_rect is not None:
			self._window_rect = window_rect
		
		if use_browser_exe is not None and browser_name_in_system is not None:
			self._detect_browser_exe(
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe
			)
	
	def _detect_browser_exe(self, browser_name_in_system: str, use_browser_exe: bool):
		if self.browser_exe is None and use_browser_exe:
			self._webdriver_flags_manager.browser_exe = get_path_to_browser(browser_name_in_system)
		elif self.browser_exe is not None and not use_browser_exe:
			self._webdriver_flags_manager.browser_exe = None
	
	@property
	def debugging_port(self) -> Optional[int]:
		return self._webdriver_flags_manager.arguments.get("remote_debugging_port", ArgumentValue(command_line="", value=None)).value
	
	@property
	def browser_exe(self) -> Optional[Union[str, pathlib.Path]]:
		return self._webdriver_flags_manager.browser_exe
	
	async def _find_debugging_port(self, debugging_port: Optional[int]) -> int:
		if self.browser_exe is not None:
			user_data_dir_command = self._webdriver_flags_manager.flags_definitions.get("user_data_dir", None)
			user_data_dir_value = self._webdriver_flags_manager.arguments.get("user_data_dir", None)
		
			user_data_dir = None if user_data_dir_command is None else user_data_dir_value.value if user_data_dir_value is not None else None
		
			if user_data_dir_command is not None:
				previous_session = await self._wrap_to_trio(
						find_browser_previous_session,
						self.browser_exe,
						user_data_dir_command.command,
						user_data_dir,
				)
				if previous_session is not None:
					return previous_session
		
		if debugging_port is not None:
			return await self._wrap_to_trio(
					get_localhost_minimum_free_port,
					console_encoding=self._console_encoding,
					ip_pattern=self._ip_pattern,
					ports_to_check=debugging_port,
			)
		
		if self.debugging_port is None or self.debugging_port == 0:
			return await self._wrap_to_trio(
					get_localhost_minimum_free_port,
					console_encoding=self._console_encoding,
					ip_pattern=self._ip_pattern,
					ports_to_check=self.debugging_port,
			)
		
		return self.debugging_port
	
	async def _set_debugging_port(self, debugging_port: Optional[int], debugging_address: Optional[str]) -> None:
		if self.browser_exe is not None:
			_debugging_address = "127.0.0.1" if debugging_address is None else debugging_address
			_debugging_port = 0 if debugging_port is None else debugging_port
		
			await self._wrap_to_trio(
					self._webdriver_flags_manager.update_flags,
					BlinkFlags(
							argument=BlinkArguments(
									remote_debugging_port=debugging_port,
									remote_debugging_address=debugging_address,
							),
							experimental_option=BlinkExperimentalOptions(debugger_address=f"{_debugging_address}:{_debugging_port}"),
					)
			)
	
	@property
	def debugging_ip(self) -> Optional[str]:
		return self._webdriver_flags_manager.arguments.get("remote_debugging_address", ArgumentValue(command_line="", value=None)).value
	
	@property
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge]]:
		return super().driver
	
	def set_start_page_url(self, start_page_url: str):
		self._webdriver_flags_manager.start_page_url = start_page_url
