import trio
import pathlib
from typing import (
	Optional,
	Type,
	Union
)
from osn_selenium.flags.blink import BlinkFlagsManager
from osn_selenium.flags.models.blink import BlinkFlags
from osn_selenium.types import (
	ARCHITECTURE_TYPEHINT,
	WindowRect
)
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)
from osn_selenium.abstract.webdriver.blink.base import (
	AbstractBlinkBaseMixin
)
from selenium.webdriver.chromium.webdriver import (
	ChromiumDriver as legacyWebDriver
)


__all__ = ["BlinkBaseMixin"]


class BlinkBaseMixin(UnifiedBlinkBaseMixin, CoreBaseMixin, AbstractBlinkBaseMixin):
	"""
	Base mixin for Blink WebDrivers handling core initialization and state management.

	This class serves as the foundation for browser-specific implementations, managing
	the WebDriver executable path, configuration flags, timeouts, and the active
	driver instance.
	"""
	
	def __init__(
			self,
			browser_exe: Optional[Union[str, pathlib.Path]],
			browser_name_in_system: str,
			webdriver_path: str,
			architecture: ARCHITECTURE_TYPEHINT,
			use_browser_exe: bool = True,
			flags_manager_type: Type[BlinkFlagsManager] = BlinkFlagsManager,
			flags: Optional[BlinkFlags] = None,
			start_page_url: str = "",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
	):
		"""
		Initializes the BlinkWebDriver instance.

		This constructor sets up the necessary components for controlling a Blink-based browser,
		including paths, flag managers, timeouts, and integration with DevTools and Trio.
		It also initializes properties related to console encoding and IP pattern matching
		for managing browser processes.

		Args:
			browser_exe (Optional[Union[str, pathlib.Path]]): The path to the browser executable
				(e.g., `chrome.exe` or `msedge.exe`). If None, the browser executable will not be
				managed directly by this class (e.g., for remote WebDriver connections where the
				browser is already running).
			browser_name_in_system (str): The common name of the browser executable in the system
				(e.g., "Chrome", "Edge"). Used to auto-detect `browser_exe` if `use_browser_exe` is True.
			webdriver_path (str): The file path to the WebDriver executable (e.g., `chromedriver.exe`).
			use_browser_exe (bool): If True, the browser executable path will be
				automatically determined based on `browser_name_in_system` if `browser_exe`
				is not explicitly provided. If False, `browser_exe` must be None.
				Defaults to True.
			flags_manager_type (Type[BlinkFlagsManager]): The type of flags manager to use.
				Defaults to `BlinkFlagsManager`, which is suitable for Chrome/Edge.
			flags (Optional[BlinkFlags]): Initial browser flags or options
				specific to Blink-based browsers. Can be a `BlinkFlags` object or a generic mapping.
				Defaults to None.
			start_page_url (str): The URL that the browser will attempt to navigate to
				immediately after starting. Defaults to an empty string.
			implicitly_wait (int): The default implicit wait time in seconds for element searches.
				Defaults to 5.
			page_load_timeout (int): The default page load timeout in seconds. Defaults to 5.
			script_timeout (int): The default asynchronous script timeout in seconds. Defaults to 5.
			window_rect (Optional[WindowRect]): The initial window size and position. If None,
				the browser's default window size will be used. Defaults to None.
			capacity_limiter (Optional[trio.CapacityLimiter]): A Trio capacity limiter used to
				throttle concurrent thread-based operations. Defaults to None.
		"""
		
		CoreBaseMixin.__init__(
				self,
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				capacity_limiter=capacity_limiter,
		)
		
		UnifiedBlinkBaseMixin.__init__(
				self,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				webdriver_path=webdriver_path,
				architecture=architecture,
				use_browser_exe=use_browser_exe,
				flags_manager_type=flags_manager_type,
				flags=flags,
				start_page_url=start_page_url,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
		)
	
	@property
	def browser_exe(self) -> Optional[Union[str, pathlib.Path]]:
		return self._browser_exe_impl
	
	@property
	def debugging_ip(self) -> Optional[str]:
		return self._debugging_ip_impl
	
	@property
	def debugging_port(self) -> Optional[int]:
		return self._debugging_port_impl
	
	@property
	def driver(self) -> Optional[legacyWebDriver]:
		return self._driver_impl
	
	def set_start_page_url(self, start_page_url: str) -> None:
		self._webdriver_flags_manager.start_page_url = start_page_url
