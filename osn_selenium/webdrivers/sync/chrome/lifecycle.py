import pathlib
from selenium import webdriver
from typing import Optional, Union
from osn_selenium.types import WindowRect
from selenium.webdriver.chrome.service import Service
from osn_selenium.flags.models.chrome import ChromeFlags
from osn_selenium.webdrivers.sync.chrome.settings import ChromeSettingsMixin
from osn_selenium.abstract.webdriver.chrome.lifecycle import (
	AbstractChromeLifecycleMixin
)


class ChromeLifecycleMixin(ChromeSettingsMixin, AbstractChromeLifecycleMixin):
	def _create_driver(self):
		webdriver_options = self._webdriver_flags_manager.options
		webdriver_service = Service(
				executable_path=self._webdriver_path,
				port=self.debugging_port if self.browser_exe is None else 0,
				service_args=self._webdriver_flags_manager.start_args
				if self.browser_exe is None
				else None
		)
		
		self._driver = webdriver.Chrome(options=webdriver_options, service=webdriver_service)
		
		if self._window_rect is not None:
			self.set_window_rect(
					x=self._window_rect.x,
					y=self._window_rect.y,
					width=self._window_rect.width,
					height=self._window_rect.height,
			)
		
		self.set_driver_timeouts(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_implicitly_wait,
		)
	
	def restart_webdriver(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		super().restart_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	def start_webdriver(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		super().start_webdriver(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
