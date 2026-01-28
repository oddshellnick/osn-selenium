import trio
from osn_selenium.models import WindowRect
from typing import (
	Mapping,
	Optional,
	Type
)
from osn_selenium.flags.chrome import ChromeFlagsManager
from osn_selenium.flags.models.chrome import ChromeFlags
from selenium.webdriver import (
	Chrome as legacyChrome
)
from osn_selenium.webdrivers.trio_threads.blink.base import BlinkBaseMixin
from osn_selenium._typehints import (
	ARCHITECTURES_TYPEHINT,
	PATH_TYPEHINT
)
from osn_selenium.webdrivers.unified.chrome.base import (
	UnifiedChromeBaseMixin
)
from osn_selenium.abstract.webdriver.chrome.base import (
	AbstractChromeBaseMixin
)


__all__ = ["ChromeBaseMixin"]


class ChromeBaseMixin(UnifiedChromeBaseMixin, BlinkBaseMixin, AbstractChromeBaseMixin):
	"""
	Base mixin for Chrome WebDrivers handling core initialization and state management.

	This class serves as the foundation for browser-specific implementations, managing
	the WebDriver executable path, configuration flags, timeouts, and the active
	driver instance.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			architecture: ARCHITECTURES_TYPEHINT,
			flags_manager_type: Type[ChromeFlagsManager] = ChromeFlagsManager,
			use_browser_exe: bool = True,
			browser_name_in_system: str = "Google Chrome",
			browser_exe: Optional[PATH_TYPEHINT] = None,
			flags: Optional[ChromeFlags] = None,
			start_page_url: str = "about:blank",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
	):
		"""
		Initializes the Trio-based Chrome WebDriver mixin with specified configuration.

		Args:
			webdriver_path (str): Path to the ChromeDriver executable.
			architecture (ARCHITECTURE_TYPEHINT): System architecture.
			flags_manager_type (Type[ChromeFlagsManager]): The class type used for managing Chrome flags.
				Defaults to ChromeFlagsManager.
			use_browser_exe (bool): Whether to use a specific browser executable path or auto-detect.
				Defaults to True.
			browser_name_in_system (str): The name of the browser in the system registry or path.
				Defaults to "Google Chrome".
			browser_exe (Optional[PATH_TYPEHINT]): Explicit path to the Chrome browser executable.
			flags (Optional[ChromeFlags]): Initial set of flags.
			start_page_url (str): The initial URL. Defaults to "about:blank".
			implicitly_wait (int): Default implicit wait time.
			page_load_timeout (int): Default page load timeout.
			script_timeout (int): Default script timeout.
			window_rect (Optional[WindowRect]): Initial window dimensions.
			capacity_limiter (Optional[trio.CapacityLimiter]): Trio capacity limiter.
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
				capacity_limiter=capacity_limiter,
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
		)
		
		UnifiedChromeBaseMixin.__init__(
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
	def driver(self) -> Optional[legacyChrome]:
		return self._driver_impl
