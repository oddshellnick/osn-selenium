from osn_selenium.models import WindowRect
from typing import (
	Mapping,
	Optional,
	Type
)
from selenium.webdriver import Edge as legacyEdge
from osn_selenium.flags.edge import EdgeFlagsManager
from osn_selenium.flags.models.edge import EdgeFlags
from osn_selenium.webdrivers.sync.blink.base import BlinkBaseMixin
from osn_selenium.webdrivers.unified.edge.base import UnifiedEdgeBaseMixin
from osn_selenium._typehints import (
	ARCHITECTURES_TYPEHINT,
	PATH_TYPEHINT
)
from osn_selenium.abstract.webdriver.edge.base import (
	AbstractEdgeBaseMixin
)


__all__ = ["EdgeBaseMixin"]


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
			architecture: ARCHITECTURES_TYPEHINT,
			flags_manager_type: Type[EdgeFlagsManager] = EdgeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Microsoft Edge",
			browser_exe: Optional[PATH_TYPEHINT] = None,
			flags: Optional[EdgeFlags] = None,
			start_page_url: str = "about:blank",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
	):
		"""
		Initializes the synchronous Edge WebDriver mixin with specified configuration.

		Args:
			webdriver_path (str): Path to the EdgeDriver executable.
			architecture (ARCHITECTURE_TYPEHINT): System architecture.
			flags_manager_type (Type[EdgeFlagsManager]): The class type used for managing Edge flags.
				Defaults to EdgeFlagsManager.
			use_browser_exe (bool): Whether to use a specific browser executable path or auto-detect.
				Defaults to True.
			browser_name_in_system (str): The name of the browser in the system registry or path.
				Defaults to "Microsoft Edge".
			browser_exe (Optional[PATH_TYPEHINT]): Explicit path to the Edge browser executable.
				If None, it may be auto-detected based on other parameters.
			flags (Optional[EdgeFlags]): Initial set of flags to configure the Edge instance.
			start_page_url (str): The URL to navigate to immediately upon startup.
				Defaults to "about:blank".
			implicitly_wait (int): Default implicit wait time in seconds. Defaults to 5.
			page_load_timeout (int): Default page load timeout in seconds. Defaults to 5.
			script_timeout (int): Default script execution timeout in seconds. Defaults to 5.
			window_rect (Optional[WindowRect]): Initial window dimensions and position.
				If None, browser defaults are used.
			cdp_versioned_packages_paths (Optional[Mapping[int, PATH_TYPEHINT]]): Custom local paths for specific CDP versions packages.
			ignore_cdp_version_package_missing (bool): Whether to ignore missing CDP package errors.
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
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
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
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
		)
	
	@property
	def driver(self) -> Optional[legacyEdge]:
		return self._driver_impl
