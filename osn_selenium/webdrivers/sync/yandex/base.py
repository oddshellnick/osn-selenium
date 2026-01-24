import pathlib
from osn_selenium.models import WindowRect
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.models.yandex import YandexFlags
from osn_selenium.flags.yandex import YandexFlagsManager
from osn_selenium._typehints import (
	ARCHITECTURE_TYPEHINT
)
from osn_selenium.webdrivers.sync.chrome.base import ChromeBaseMixin
from osn_selenium.webdrivers.unified.yandex.base import (
	UnifiedYandexBaseMixin
)
from osn_selenium.abstract.webdriver.yandex.base import (
	AbstractYandexBaseMixin
)


__all__ = ["YandexBaseMixin"]


class YandexBaseMixin(UnifiedYandexBaseMixin, ChromeBaseMixin, AbstractYandexBaseMixin):
	"""
	Base mixin for Yandex WebDrivers handling core initialization and state management.

	This class serves as the foundation for browser-specific implementations, managing
	the WebDriver executable path, configuration flags, timeouts, and the active
	driver instance.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			architecture: ARCHITECTURE_TYPEHINT,
			flags_manager_type: Type[YandexFlagsManager] = YandexFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Yandex",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[YandexFlags] = None,
			start_page_url: str = "about:blank",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
	):
		"""
		Initializes the synchronous Yandex WebDriver mixin with specified configuration.

		Args:
			webdriver_path (str): Path to the YandexDriver executable.
			architecture (ARCHITECTURE_TYPEHINT): System architecture.
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
				Defaults to "about:blank".
			implicitly_wait (int): Default implicit wait time in seconds. Defaults to 5.
			page_load_timeout (int): Default page load timeout in seconds. Defaults to 5.
			script_timeout (int): Default script execution timeout in seconds. Defaults to 5.
			window_rect (Optional[WindowRect]): Initial window dimensions and position.
				If None, browser defaults are used.
		"""
		
		ChromeBaseMixin.__init__(
				self,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				webdriver_path=webdriver_path,
				architecture=architecture,
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
		)
		
		UnifiedYandexBaseMixin.__init__(
				self,
				webdriver_path=webdriver_path,
				architecture=architecture,
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
		)
