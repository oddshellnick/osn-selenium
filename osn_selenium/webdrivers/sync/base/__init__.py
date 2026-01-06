from typing import Optional, Type
from osn_selenium.types import WindowRect
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.executors.sync.cdp import CDPExecutor
from osn_selenium.webdrivers.sync.base.auth import AuthMixin
from osn_selenium.webdrivers.sync.base.file import FileMixin
from osn_selenium.executors.sync.javascript import JSExecutor
from osn_selenium.webdrivers.sync.base.script import ScriptMixin
from osn_selenium.webdrivers.sync.base.window import WindowMixin
from osn_selenium.abstract.webdriver.base import AbstractWebDriver
from osn_selenium.webdrivers.sync.base.actions import ActionsMixin
from osn_selenium.webdrivers.sync.base.capture import CaptureMixin
from osn_selenium.webdrivers.sync.base.element import ElementMixin
from osn_selenium.webdrivers.sync.base.storage import StorageMixin
from osn_selenium.webdrivers.sync.base.devtools import DevToolsMixin
from osn_selenium.webdrivers.sync.base.lifecycle import LifecycleMixin
from osn_selenium.webdrivers.sync.base.comonents import ComponentsMixin
from osn_selenium.webdrivers.sync.base.navigation import NavigationMixin


class WebDriver(
		ActionsMixin,
		AuthMixin,
		CaptureMixin,
		ComponentsMixin,
		DevToolsMixin,
		ElementMixin,
		FileMixin,
		LifecycleMixin,
		NavigationMixin,
		StorageMixin,
		WindowMixin,
		AbstractWebDriver
):
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
		
		self._cdp_executor = CDPExecutor(execute_function=self.execute_cdp_cmd)
	
	@property
	def cdp(self) -> CDPExecutor:
		return self._cdp_executor
	
	@property
	def javascript(self) -> JSExecutor:
		return self._js_executor
