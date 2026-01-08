import pathlib
from selenium import webdriver
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.models.chrome import ChromeFlags
from osn_selenium.flags.chrome import ChromeFlagsManager
from osn_selenium.webdrivers.sync.blink import BlinkWebDriver
from osn_selenium.abstract.webdriver.chrome.base import (
	AbstractChromeBaseMixin
)


class ChromeBaseMixin(BlinkWebDriver, AbstractChromeBaseMixin):
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[ChromeFlagsManager] = ChromeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Google Chrome",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[ChromeFlags] = None,
			start_page_url: str = "https://www.chrome.com",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
	):
		"""
		Initializes the synchronous Chrome WebDriver mixin with specified configuration.

		Args:
			webdriver_path (str): Path to the ChromeDriver executable.
			flags_manager_type (Type[ChromeFlagsManager]): The class type used for managing Chrome flags.
				Defaults to ChromeFlagsManager.
			use_browser_exe (bool): Whether to use a specific browser executable path or auto-detect.
				Defaults to True.
			browser_name_in_system (str): The name of the browser in the system registry or path.
				Defaults to "Chrome".
			browser_exe (Optional[Union[str, pathlib.Path]]): Explicit path to the Chrome browser executable.
				If None, it may be auto-detected based on other parameters.
			flags (Optional[ChromeFlags]): Initial set of flags to configure the Chrome instance.
			start_page_url (str): The URL to navigate to immediately upon startup.
				Defaults to "https://www.chrome.com".
			implicitly_wait (int): Default implicit wait time in seconds. Defaults to 5.
			page_load_timeout (int): Default page load timeout in seconds. Defaults to 5.
			script_timeout (int): Default script execution timeout in seconds. Defaults to 5.
			window_rect (Optional[WindowRect]): Initial window dimensions and position.
				If None, browser defaults are used.
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
		)
	
	@property
	def driver(self) -> Optional[webdriver.Chrome]:
		return super().driver
