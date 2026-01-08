import pathlib
import warnings
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.blink import BlinkFlags
from osn_selenium.webdrivers.sync.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink.settings import (
	AbstractBlinkSettingsMixin
)


class BlinkSettingsMixin(BlinkBaseMixin, AbstractBlinkSettingsMixin):
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
