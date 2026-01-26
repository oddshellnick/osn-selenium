import pathlib
from typing import Mapping, Optional, Type
from osn_selenium.models import WindowRect
from osn_selenium.flags.blink import BlinkFlagsManager
from osn_selenium.flags.models.values import ArgumentValue
from osn_selenium.browsers_handler import get_path_to_browser
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from osn_selenium._typehints import (
	ARCHITECTURES_TYPEHINT,
	PATH_TYPEHINT
)
from selenium.webdriver.chromium.webdriver import (
	ChromiumDriver as legacyWebDriver
)
from osn_selenium.webdrivers._executable_tables.functions import (
	find_browser_previous_session
)
from osn_selenium.flags.models.blink import (
	BlinkArguments,
	BlinkExperimentalOptions,
	BlinkFlags
)
from osn_system_utils.api.network import (
	get_localhost_free_port_of,
	get_random_localhost_free_port
)


__all__ = ["UnifiedBlinkBaseMixin"]


class UnifiedBlinkBaseMixin(UnifiedCoreBaseMixin):
	def __init__(
			self,
			browser_exe: Optional[PATH_TYPEHINT],
			browser_name_in_system: str,
			webdriver_path: str,
			architecture: ARCHITECTURES_TYPEHINT,
			use_browser_exe: bool = True,
			flags_manager_type: Type[BlinkFlagsManager] = BlinkFlagsManager,
			flags: Optional[BlinkFlags] = None,
			start_page_url: str = "",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
	):
		UnifiedCoreBaseMixin.__init__(
				self,
				webdriver_path=webdriver_path,
				architecture=architecture,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
		)
		
		if browser_exe is not None:
			self._webdriver_flags_manager.browser_exe = browser_exe
		
		if start_page_url is not None:
			self._webdriver_flags_manager.start_page_url = start_page_url
		
		if window_rect is not None:
			self._window_rect = window_rect
		
		if use_browser_exe is not None and browser_name_in_system is not None:
			self._detect_browser_exe_impl(
					browser_name_in_system=browser_name_in_system,
					use_browser_exe=use_browser_exe
			)
	
	def _detect_browser_exe_impl(self, browser_name_in_system: str, use_browser_exe: bool) -> None:
		if self._browser_exe_impl is None and use_browser_exe:
			self._webdriver_flags_manager.browser_exe = get_path_to_browser(browser_name_in_system)
		elif self._browser_exe_impl is not None and not use_browser_exe:
			self._webdriver_flags_manager.browser_exe = None
	
	@property
	def _debugging_ip_impl(self) -> Optional[str]:
		return self._webdriver_flags_manager.arguments.get("remote_debugging_address", ArgumentValue(command_line="", value=None)).value
	
	@property
	def _driver_impl(self) -> Optional[legacyWebDriver]:
		return super()._driver_impl
	
	@property
	def _debugging_port_impl(self) -> Optional[int]:
		return self._webdriver_flags_manager.arguments.get("remote_debugging_port", ArgumentValue(command_line="", value=None)).value
	
	@property
	def _browser_exe_impl(self) -> Optional[pathlib.Path]:
		return self._webdriver_flags_manager.browser_exe
	
	def _find_debugging_port_impl(self, debugging_port: Optional[int]) -> int:
		if self._browser_exe_impl is not None:
			user_data_dir_command = self._webdriver_flags_manager.flags_definitions.get("user_data_dir", None)
			user_data_dir_value = self._webdriver_flags_manager.arguments.get("user_data_dir", None)
		
			user_data_dir = None if user_data_dir_command is None else user_data_dir_value.value if user_data_dir_value is not None else None
		
			if user_data_dir_command is not None:
				previous_session = find_browser_previous_session(self._browser_exe_impl, user_data_dir_command.command, user_data_dir)
		
				if previous_session is not None:
					return previous_session
		
		if debugging_port is not None:
			return get_localhost_free_port_of(ports_to_check=debugging_port, on_candidates="min")
		
		if self._debugging_port_impl is None or self._debugging_port_impl == 0:
			return get_random_localhost_free_port()
		
		return self._debugging_port_impl
	
	def _set_debugging_port_impl(self, debugging_port: Optional[int], debugging_address: Optional[str]) -> None:
		if self._browser_exe_impl is not None:
			_debugging_address = "127.0.0.1" if debugging_address is None else debugging_address
			_debugging_port = 0 if debugging_port is None else debugging_port
		
			self._webdriver_flags_manager.update_flags(
					BlinkFlags(
							argument=BlinkArguments(
									remote_debugging_port=debugging_port,
									remote_debugging_address=debugging_address,
							),
							experimental_option=BlinkExperimentalOptions(debugger_address=f"{_debugging_address}:{_debugging_port}"),
					)
			)
