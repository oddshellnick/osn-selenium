import trio
import pathlib
from typing import (
	Optional,
	Type,
	Union
)
from selenium.webdriver import Edge as legacyEdge
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.flags.edge import EdgeFlagsManager
from osn_selenium.types import (
	ARCHITECTURE_TYPEHINT,
	WindowRect
)
from osn_selenium.webdrivers.trio_threads.blink.base import BlinkBaseMixin
from osn_selenium.webdrivers.unified.edge.base import UnifiedEdgeBaseMixin
from osn_selenium.abstract.webdriver.edge.base import (
	AbstractEdgeBaseMixin
)


class EdgeBaseMixin(UnifiedEdgeBaseMixin, BlinkBaseMixin, AbstractEdgeBaseMixin):
	"""
	Base mixin for Edge WebDrivers handling core initialization and state management.

	This class serves as the foundation for browser-specific implementations, managing
	the WebDriver executable path, configuration flags, timeouts, and the active
	driver instance.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			architecture: ARCHITECTURE_TYPEHINT,
			flags_manager_type: Type[EdgeFlagsManager] = EdgeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Microsoft Edge",
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			flags: Optional[EdgeFlags] = None,
			start_page_url: str = "about:blank",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
	):
		"""
		Initializes the Trio-based Edge WebDriver mixin.

		Args:
			webdriver_path (str): Path to the EdgeDriver executable.
			architecture (ARCHITECTURE_TYPEHINT): System architecture.
			flags_manager_type (Type[EdgeFlagsManager]): The class type used for managing Edge flags.
				Defaults to EdgeFlagsManager.
			use_browser_exe (bool): Whether to use a specific browser executable path or auto-detect.
				Defaults to True.
			browser_name_in_system (str): The name of the browser in the system registry or path.
				Defaults to "Microsoft Edge".
			browser_exe (Optional[Union[str, pathlib.Path]]): Explicit path to the Edge browser executable.
			flags (Optional[EdgeFlags]): Initial set of flags.
			start_page_url (str): The initial URL. Defaults to "about:blank".
			implicitly_wait (int): Default implicit wait time.
			page_load_timeout (int): Default page load timeout.
			script_timeout (int): Default script timeout.
			window_rect (Optional[WindowRect]): Initial window dimensions.
			capacity_limiter (Optional[trio.CapacityLimiter]): Trio capacity limiter.
		"""
		
		BlinkBaseMixin.__init__(
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
				capacity_limiter=capacity_limiter,
		)
		
		UnifiedEdgeBaseMixin.__init__(
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
	
	@property
	def driver(self) -> Optional[legacyEdge]:
		return self._driver_impl
