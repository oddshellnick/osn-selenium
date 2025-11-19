import pathlib

from osn_selenium.abstract.webdriver.yandex import AbstractYandexWebDriver
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.utils.yandex import YandexFlags
from osn_selenium.flags.yandex import YandexFlagsManager
from osn_selenium.dev_tools.manager import DevToolsSettings
from osn_selenium.webdrivers.sync.chrome import ChromeWebDriver


class YandexWebDriver(ChromeWebDriver, AbstractYandexWebDriver):
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[YandexFlagsManager] = YandexFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Yandex",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[YandexFlags] = None,
			start_page_url: str = "https://www.yandex.com",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
	):
		"""
		Initializes a YandexWebDriver instance.

		This constructor prepares the Yandex Browser for automation by setting up
		its executable path, WebDriver path, browser flags, and other operational
		settings. It leverages the `BlinkWebDriver` base class for common Chromium-based
		browser functionalities.

		Args:
			webdriver_path (str): The file path to the ChromeDriver executable.
			flags_manager_type (Type[YandexFlagsManager]): The type of flags manager
				to use for configuring Yandex Browser-specific command-line arguments.
				Defaults to `YandexFlagsManager`.
			use_browser_exe (bool): If True, the browser executable path will be
				automatically determined based on `browser_name_in_system` if `browser_exe`
				is not explicitly provided. If False, `browser_exe` must be None.
				Defaults to True.
			browser_name_in_system (str): The common name of the Yandex Browser
				executable in the system (e.g., "Yandex"). Used to auto-detect `browser_exe`.
				Defaults to "Yandex".
			browser_exe (Optional[Union[str, pathlib.Path]]): The explicit path to the
				Yandex Browser executable. If `use_browser_exe` is True and this is None,
				it will attempt to find the browser automatically. If `use_browser_exe`
				is False, this must be None.
			flags (Optional[YandexFlags]): An object containing specific flags or options
				to pass to the Yandex Browser process.
			start_page_url (str): The URL to load when the browser session starts.
				Defaults to "https://www.yandex.com".
			implicitly_wait (int): The default implicit wait time in seconds for the WebDriver.
				Defaults to 5 seconds.
			page_load_timeout (int): The default timeout in seconds for page loading.
				Defaults to 5 seconds.
			script_timeout (int): The default timeout in seconds for asynchronous JavaScript execution.
				Defaults to 5 seconds.
			window_rect (Optional[WindowRect]): An object specifying the initial window
				position and size.
			devtools_settings (Optional[DevToolsSettings]): Settings for configuring the
				Chrome DevTools Protocol (CDP) interface.
		"""
		
		super().__init__(
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				use_browser_exe=use_browser_exe,
				browser_name_in_system=browser_name_in_system,
				browser_exe=browser_exe,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				devtools_settings=devtools_settings,
		)
	
	def reset_settings(
			self,
			flags: Optional[YandexFlags] = None,
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
	
	def update_settings(
			self,
			flags: Optional[YandexFlags] = None,
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
