import trio
from osn_selenium.models import WindowRect
from typing import (
	Mapping,
	Optional,
	Type
)
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.blink import BlinkFlagsManager
from osn_selenium.flags.models.blink import BlinkFlags
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.webdrivers.trio_threads.core import CoreWebDriver
from osn_selenium.webdrivers.trio_threads.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink import (
	AbstractBlinkWebDriver
)
from osn_selenium.webdrivers.trio_threads.blink.casting import BlinkCastingMixin
from osn_selenium.webdrivers.trio_threads.blink.logging import BlinkLoggingMixin
from osn_selenium.webdrivers.trio_threads.blink.network import BlinkNetworkMixin
from osn_selenium.webdrivers.trio_threads.blink.features import BlinkFeaturesMixin
from osn_selenium.webdrivers.trio_threads.blink.settings import BlinkSettingsMixin
from osn_selenium.webdrivers.trio_threads.blink.lifecycle import BlinkLifecycleMixin


__all__ = ["BlinkWebDriver"]


class BlinkWebDriver(
		BlinkBaseMixin,
		BlinkCastingMixin,
		BlinkFeaturesMixin,
		BlinkLifecycleMixin,
		BlinkLoggingMixin,
		BlinkNetworkMixin,
		BlinkSettingsMixin,
		CoreWebDriver,
		AbstractBlinkWebDriver,
):
	"""
	Concrete Blink WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	def __init__(
			self,
			browser_exe: Optional[PATH_TYPEHINT],
			browser_name_in_system: str,
			webdriver_path: str,
			use_browser_exe: bool = True,
			flags_manager_type: Type[BlinkFlagsManager] = BlinkFlagsManager,
			flags: Optional[BlinkFlags] = None,
			start_page_url: str = "",
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
	):
		"""
		Initializes the BlinkWebDriver instance.

		This constructor sets up the necessary components for controlling a Blink-based browser,
		including paths, flag managers, timeouts, and integration with DevTools and Trio.
		It also initializes properties related to console encoding and IP pattern matching
		for managing browser processes.

		Args:
			browser_exe (Optional[PATH_TYPEHINT]): The path to the browser executable
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
			devtools_settings (Optional[DevToolsSettings]): Configuration for Chrome DevTools Protocol.
			capacity_limiter (Optional[trio.CapacityLimiter]): A Trio capacity limiter used to
				throttle concurrent thread-based operations. Defaults to None.
		"""
		
		CoreWebDriver.__init__(
				self,
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				devtools_settings=devtools_settings,
				capacity_limiter=capacity_limiter,
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
		)
		
		BlinkBaseMixin.__init__(
				self,
				browser_exe=browser_exe,
				browser_name_in_system=browser_name_in_system,
				use_browser_exe=use_browser_exe,
				webdriver_path=webdriver_path,
				architecture="trio_threads",
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
