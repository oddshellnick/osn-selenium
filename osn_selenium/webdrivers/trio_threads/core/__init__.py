import trio
from osn_selenium.models import WindowRect
from typing import (
	Mapping,
	Optional,
	Type
)
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.dev_tools.manager import DevTools
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.webdrivers.trio_threads.core.auth import CoreAuthMixin
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.webdrivers.trio_threads.core.file import CoreFileMixin
from osn_selenium.abstract.webdriver.core import (
	AbstractCoreWebDriver
)
from osn_selenium.webdrivers.trio_threads.core.script import CoreScriptMixin
from osn_selenium.webdrivers.trio_threads.core.window import CoreWindowMixin
from osn_selenium.webdrivers.trio_threads.core.actions import CoreActionsMixin
from osn_selenium.webdrivers.trio_threads.core.capture import CoreCaptureMixin
from osn_selenium.webdrivers.trio_threads.core.element import CoreElementMixin
from osn_selenium.webdrivers.trio_threads.core.storage import CoreStorageMixin
from osn_selenium.webdrivers.trio_threads.core.devtools import CoreDevToolsMixin
from osn_selenium.webdrivers.trio_threads.core.settings import CoreSettingsMixin
from osn_selenium.webdrivers.trio_threads.core.timeouts import CoreTimeoutsMixin
from osn_selenium.webdrivers.trio_threads.core.lifecycle import CoreLifecycleMixin
from osn_selenium.webdrivers.trio_threads.core.comonents import CoreComponentsMixin
from osn_selenium.webdrivers.trio_threads.core.navigation import CoreNavigationMixin


__all__ = ["CoreWebDriver"]


class CoreWebDriver(
		CoreActionsMixin,
		CoreAuthMixin,
		CoreBaseMixin,
		CoreCaptureMixin,
		CoreComponentsMixin,
		CoreDevToolsMixin,
		CoreElementMixin,
		CoreFileMixin,
		CoreLifecycleMixin,
		CoreNavigationMixin,
		CoreScriptMixin,
		CoreSettingsMixin,
		CoreStorageMixin,
		CoreTimeoutsMixin,
		CoreWindowMixin,
		AbstractCoreWebDriver,
):
	"""
	Concrete Core WebDriver implementation combining all functional mixins.

	This class aggregates lifecycle management, element interaction, navigation,
	and browser-specific features into a single usable driver instance.
	"""
	
	def __init__(
			self,
			webdriver_path: str,
			flags_manager_type: Type[BrowserFlagsManager] = BrowserFlagsManager,
			flags: Optional[BrowserFlags] = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			script_timeout: int = 5,
			window_rect: Optional[WindowRect] = None,
			devtools_settings: Optional[DevToolsSettings] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
			cdp_versioned_packages_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_cdp_version_package_missing: bool = True,
	) -> None:
		"""
		Initializes the main WebDriver instance with Trio thread support.

		Args:
			webdriver_path (str): The file path to the WebDriver executable.
			flags_manager_type (Type[BrowserFlagsManager]): The class type used to manage
				browser-specific configuration flags. Defaults to BrowserFlagsManager.
			flags (Optional[BrowserFlags]): Initial set of browser flags or options
				to apply upon startup. Defaults to None.
			implicitly_wait (int): The amount of time (in seconds) that the driver should
				wait when searching for elements. Defaults to 5.
			page_load_timeout (int): The amount of time (in seconds) to wait for a page
				load to complete. Defaults to 5.
			script_timeout (int): The amount of time (in seconds) to wait for an
				asynchronous script to finish execution. Defaults to 5.
			window_rect (Optional[WindowRect]): The initial size and position of the
				browser window. Defaults to None.
			devtools_settings (Optional[DevToolsSettings]): Configuration for Chrome DevTools Protocol.
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
				cdp_versioned_packages_paths=cdp_versioned_packages_paths,
				ignore_cdp_version_package_missing=ignore_cdp_version_package_missing,
		)
		
		self._devtools = DevTools(parent_webdriver=self, devtools_settings=devtools_settings)
	
	@property
	def devtools(self) -> DevTools:
		return self._devtools
