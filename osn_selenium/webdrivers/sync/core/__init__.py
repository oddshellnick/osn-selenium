from typing import Optional, Type
from osn_selenium.types import WindowRect
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.executors.sync.javascript import JSExecutor
from osn_selenium.webdrivers.sync.core.auth import CoreAuthMixin
from osn_selenium.webdrivers.sync.core.file import CoreFileMixin
from osn_selenium.webdrivers.sync.core.window import CoreWindowMixin
from osn_selenium.webdrivers.sync.core.actions import CoreActionsMixin
from osn_selenium.webdrivers.sync.core.capture import CoreCaptureMixin
from osn_selenium.webdrivers.sync.core.element import CoreElementMixin
from osn_selenium.webdrivers.sync.core.storage import CoreStorageMixin
from osn_selenium.webdrivers.sync.core.devtools import CoreDevToolsMixin
from osn_selenium.webdrivers.sync.core.lifecycle import CoreLifecycleMixin
from osn_selenium.abstract.webdriver.core import (
	AbstractCoreWebDriver
)
from osn_selenium.webdrivers.sync.core.comonents import CoreComponentsMixin
from osn_selenium.webdrivers.sync.core.navigation import CoreNavigationMixin


class CoreWebDriver(
		CoreActionsMixin,
		CoreAuthMixin,
		CoreCaptureMixin,
		CoreComponentsMixin,
		CoreDevToolsMixin,
		CoreElementMixin,
		CoreFileMixin,
		CoreLifecycleMixin,
		CoreNavigationMixin,
		CoreStorageMixin,
		CoreWindowMixin,
		AbstractCoreWebDriver
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
	) -> None:
		"""
		Initializes the synchronous WebDriver instance.

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
		"""
		
		super().__init__(
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
		)
		
		self._js_executor = JSExecutor(execute_function=self.execute_script)
	
	@property
	def javascript(self) -> JSExecutor:
		return self._js_executor
