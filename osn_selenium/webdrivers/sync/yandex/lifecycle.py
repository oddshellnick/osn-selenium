import pathlib
from typing import Optional, Union
from osn_selenium.types import WindowRect
from osn_selenium.flags.models.yandex import YandexFlags
from osn_selenium.webdrivers.sync.yandex.settings import YandexSettingsMixin
from osn_selenium.abstract.webdriver.yandex.lifecycle import (
	AbstractYandexLifecycleMixin
)


class YandexLifecycleMixin(YandexSettingsMixin, AbstractYandexLifecycleMixin):
	"""
	Mixin for managing the lifecycle of the Yandex WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	def restart_webdriver(
			self,
			flags: Optional[YandexFlags] = None,
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
			flags: Optional[YandexFlags] = None,
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
