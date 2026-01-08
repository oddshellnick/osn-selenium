import pathlib
from selenium import webdriver
from osn_selenium.types import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.flags.edge import EdgeFlagsManager
from osn_selenium.webdrivers.sync.blink import BlinkWebDriver
from osn_selenium.abstract.webdriver.edge.base import (
	AbstractEdgeBaseMixin
)


class EdgeBaseMixin(BlinkWebDriver, AbstractEdgeBaseMixin):
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[EdgeFlagsManager] = EdgeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Edge",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[EdgeFlags] = None,
			start_page_url: str = "https://www.chrome.com",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
	):
		"""
		Initializes the synchronous Edge WebDriver mixin with specified configuration.
		
		Args:
			webdriver_path (str): Path to the EdgeDriver executable.
			flags_manager_type (Type[EdgeFlagsManager]): The class type used for managing Edge flags.
				Defaults to EdgeFlagsManager.
			use_browser_exe (bool): Whether to use a specific browser executable path or auto-detect.
				Defaults to True.
			browser_name_in_system (str): The name of the browser in the system registry or path.
				Defaults to "Edge".
			browser_exe (Optional[Union[str, pathlib.Path]]): Explicit path to the Edge browser executable.
				If None, it may be auto-detected based on other parameters.
			flags (Optional[EdgeFlags]): Initial set of flags to configure the Edge instance.
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
	def driver(self) -> Optional[webdriver.Edge]:
		return super().driver
