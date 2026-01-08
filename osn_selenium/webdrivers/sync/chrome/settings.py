import pathlib
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.chrome import ChromeFlags
from osn_selenium.webdrivers.sync.chrome.base import ChromeBaseMixin
from osn_selenium.abstract.webdriver.chrome.settings import (
	AbstractChromeSettingsMixin
)


class ChromeSettingsMixin(ChromeBaseMixin, AbstractChromeSettingsMixin):
	def reset_settings(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: str = "",
			window_rect: Optional[WindowRect] = None,
	):
		super().reset_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
	
	def update_settings(
			self,
			flags: Optional[ChromeFlags] = None,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			browser_name_in_system: Optional[str] = None,
			use_browser_exe: Optional[bool] = None,
			start_page_url: Optional[str] = None,
			window_rect: Optional[WindowRect] = None,
	):
		super().update_settings(
				flags=flags,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				start_page_url=start_page_url,
				window_rect=window_rect,
		)
