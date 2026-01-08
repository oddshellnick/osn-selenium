import trio
import pathlib
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.models.yandex import YandexFlags
from osn_selenium.flags.yandex import YandexFlagsManager
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.webdrivers.trio_threads.chrome import ChromeWebDriver
from osn_selenium.abstract.webdriver.yandex.base import (
	AbstractYandexBaseMixin
)


class YandexBaseMixin(ChromeWebDriver, AbstractYandexBaseMixin):
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[YandexFlagsManager] = YandexFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Yandex",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[YandexFlags] = None,
			start_page_url: str = "https://www.chrome.com",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
	) -> None:
		"""
		Initializes the asynchronous (Trio) Yandex WebDriver mixin with specified configuration.
		
		Args:
			webdriver_path (str): Path to the YandexDriver executable.
			flags_manager_type (Type[YandexFlagsManager]): The class type used for managing Yandex flags.
				Defaults to YandexFlagsManager.
			use_browser_exe (bool): Whether to use a specific browser executable path or auto-detect.
				Defaults to True.
			browser_name_in_system (str): The name of the browser in the system registry or path.
				Defaults to "Yandex".
			browser_exe (Optional[Union[str, pathlib.Path]]): Explicit path to the Yandex browser executable.
				If None, it may be auto-detected based on other parameters.
			flags (Optional[YandexFlags]): Initial set of flags to configure the Yandex instance.
			start_page_url (str): The URL to navigate to immediately upon startup.
				Defaults to "https://www.chrome.com".
			implicitly_wait (int): Default implicit wait time in seconds. Defaults to 5.
			page_load_timeout (int): Default page load timeout in seconds. Defaults to 5.
			script_timeout (int): Default script execution timeout in seconds. Defaults to 5.
			window_rect (Optional[WindowRect]): Initial window dimensions and position.
				If None, browser defaults are used.
			devtools_settings (Optional[DevToolsSettings]): Configuration for Chrome DevTools Protocol.
			capacity_limiter (Optional[trio.CapacityLimiter]): Trio capacity limiter for concurrency control.
		"""
		
		super().__init__(
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				devtools_settings=devtools_settings,
				capacity_limiter=capacity_limiter,
		)
