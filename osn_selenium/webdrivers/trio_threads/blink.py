import re
import sys
import trio
import pathlib
import warnings
from subprocess import Popen

from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.types import WindowRect
from osn_selenium.flags.base import ArgumentValue
from osn_selenium.flags.blink import BlinkFlagsManager
from osn_windows_cmd.taskkill.parameters import TaskKillTypes
from osn_selenium.browsers_handler import get_path_to_browser
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.base import WebDriver
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Type,
	Union
)
from osn_windows_cmd.taskkill import (
	ProcessID,
	taskkill_windows
)
from osn_selenium.abstract.webdriver.blink import (
	AbstractBlinkWebDriver
)
from osn_selenium.webdrivers._functions import (
	find_browser_previous_session
)
from selenium.webdriver.chromium.webdriver import (
	ChromiumDriver as legacyWebDriver
)
from osn_selenium.flags.models.blink import (
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
			devtools_settings: Optional[DevToolsSettings] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
	) -> None:
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
				devtools_settings=devtools_settings,
				capacity_limiter=capacity_limiter,
		)
		
		if browser_exe is not None:
			self._webdriver_flags_manager.browser_exe = browser_exe
		
		if start_page_url is not None:
			self.set_start_page_url(start_page_url)
		
		if use_browser_exe is not None and browser_name_in_system is not None:
			self._detect_browser_exe(
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
			)
	
	@requires_driver
	async def delete_network_conditions(self) -> None:
		return await self._wrap_to_trio(self.driver.delete_network_conditions)
	
	@requires_driver
	async def get_issue_message(self) -> str:
		return await self._wrap_to_trio(self.driver.get_issue_message)
	
	@requires_driver
	async def get_log(self, log_type: str):
		return await self._wrap_to_trio(self.driver.get_log, log_type=log_type)
	
	@requires_driver
	async def get_network_conditions(self) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.get_network_conditions)
	
	@requires_driver
	async def get_sinks(self) -> List[str]:
		return await self._wrap_to_trio(self.driver.get_sinks)
	
	@requires_driver
	async def launch_app(self, id: str) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.launch_app, id=id)
	
	@requires_driver
	async def log_types(self) -> List[str]:
		return await self._wrap_to_trio(lambda: self.driver.log_types)
	
	@property
	def debugging_port(self) -> Optional[int]:
		return self._webdriver_flags_manager.arguments.get("remote_debugging_port", ArgumentValue(command_line="", value=None),).value
	
	@property
	def browser_exe(self) -> Optional[pathlib.Path]:
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
	
	def _detect_browser_exe(self, browser_name_in_system: str, use_browser_exe: bool) -> None:
		if self.browser_exe is None and use_browser_exe:
			self._webdriver_flags_manager.browser_exe = get_path_to_browser(browser_name_in_system)
		elif self.browser_exe is not None and not use_browser_exe:
			self._webdriver_flags_manager.browser_exe = None
	
	def set_start_page_url(self, start_page_url: str) -> None:
		self._webdriver_flags_manager.start_page_url = start_page_url
	
	async def reset_settings(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if not self.is_active:
			if window_rect is None:
				window_rect = await self._wrap_to_trio(WindowRect)
		
			if flags is not None:
				await self._wrap_to_trio(self._webdriver_flags_manager.set_flags, flags)
			else:
				await self._wrap_to_trio(self._webdriver_flags_manager.clear_flags)
		
			self._webdriver_flags_manager.browser_exe = browser_exe
		
			await self._wrap_to_trio(self.set_start_page_url, start_page_url)
			self._window_rect = window_rect
		
			if use_browser_exe is not None and browser_name_in_system is not None:
				await self._wrap_to_trio(
						self._detect_browser_exe,
						browser_name_in_system=browser_name_in_system,
						use_browser_exe=use_browser_exe,
				)
		
			if self.browser_exe is not None and self.debugging_port is not None or self.debugging_ip is not None:
				await self._set_debugging_port(await self._find_debugging_port(self.debugging_port), self.debugging_ip,)
		else:
			warnings.warn("Browser is already running.")
	
	async def _create_driver(self) -> None:
		await super()._create_driver()
	
	async def _check_browser_exe_active(self) -> bool:
		pids_with_addrs = await self._wrap_to_trio(
				get_localhost_pids_with_addresses,
				self._console_encoding,
				self._ip_pattern,
		)
		
		for pid, ports in pids_with_addrs.items():
			if len(ports) == 1 and re.search(rf":{self.debugging_port}\Z", ports[0]) is not None:
				address = re.search(rf"\A(.+):{self.debugging_port}\Z", ports[0]).group(1)
		
				if address != self.debugging_ip:
					await self._set_debugging_port(debugging_port=self.debugging_port, debugging_address=address,)
		
				return True
		
		return False
	
	async def update_settings(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if flags is not None:
			await self._wrap_to_trio(self._webdriver_flags_manager.update_flags, flags)
		
		if browser_exe is not None:
			self._webdriver_flags_manager.browser_exe = browser_exe
		
		if start_page_url is not None:
			await self._wrap_to_trio(self.set_start_page_url, start_page_url)
		
		if window_rect is not None:
			self._window_rect = window_rect
		
		if use_browser_exe is not None and browser_name_in_system is not None:
			self._detect_browser_exe(
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
			)
		
		await self._set_debugging_port(await self._find_debugging_port(self.debugging_port), self.debugging_ip)
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return super().driver
	
	async def start_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if self.driver is None:
			await self.update_settings(
					flags=flags,
					browser_exe=browser_exe,
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe,
					start_page_url=start_page_url,
					window_rect=window_rect,
			)
		
			if self.browser_exe is not None:
				is_active = await self._check_browser_exe_active()
		
				if not is_active:
					await self._wrap_to_trio(Popen, args=self._webdriver_flags_manager.start_command, shell=True)
		
					while not is_active:
						is_active = await self._check_browser_exe_active()
		
						if not is_active:
							await trio.sleep(0.05)
		
			await self._create_driver()

			self._is_active = True
	
	async def close_webdriver(self) -> None:
		if self.browser_exe is not None:
			pids_to_ports = await self._wrap_to_trio(
					get_localhost_pids_with_ports,
					self._console_encoding,
					self._ip_pattern,
			)
		
			for pid, ports in pids_to_ports.items():
				if ports == [self.debugging_port]:
					await self._wrap_to_trio(
							taskkill_windows,
							taskkill_type=TaskKillTypes.forcefully_terminate,
							selectors=ProcessID(pid),
					)
		
					is_active = await self._check_browser_exe_active()
		
					while is_active:
						is_active = await self._check_browser_exe_active()
		
						if is_active:
							await trio.sleep(0.05)
		
		if self.driver is not None:
			await self.quit()
			self._driver = None

		self._is_active = False
	
	async def restart_webdriver(
			self,
			flags: Optional[BlinkFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.close_webdriver()
		await self.start_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	@requires_driver
	async def set_network_conditions(self, **network_conditions: Dict[str, Any]) -> None:
		return await self._wrap_to_trio(self.driver.set_network_conditions, **network_conditions)
	
	@requires_driver
	async def set_permissions(self, name: str, value: str) -> None:
		return await self._wrap_to_trio(self.driver.set_permissions, name=name, value=value)
	
	@requires_driver
	async def set_sink_to_use(self, sink_name: str) -> Dict:
		return await self._wrap_to_trio(self.driver.set_sink_to_use, sink_name=sink_name)
	
	@requires_driver
	async def start_desktop_mirroring(self, sink_name: str) -> Dict:
		return await self._wrap_to_trio(self.driver.start_desktop_mirroring, sink_name=sink_name)
	
	@requires_driver
	async def start_tab_mirroring(self, sink_name: str) -> Dict:
		return await self._wrap_to_trio(self.driver.start_tab_mirroring, sink_name=sink_name)
	
	@requires_driver
	async def stop_casting(self, sink_name: str) -> Dict:
		return await self._wrap_to_trio(self.driver.stop_casting, sink_name=sink_name)
