import trio
from typing import Optional, Type
from osn_selenium.types import WindowRect
from osn_selenium.dev_tools.manager import DevTools
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.dev_tools.settings import DevToolsSettings
from osn_selenium.executors.trio_threads.cdp import CDPExecutor
from osn_selenium.abstract.webdriver.base import AbstractWebDriver
from osn_selenium.webdrivers.trio_threads.base.auth import AuthMixin
from osn_selenium.webdrivers.trio_threads.base.file import FileMixin
from osn_selenium.executors.trio_threads.javascript import JSExecutor
from osn_selenium.webdrivers.trio_threads.base.window import WindowMixin
from osn_selenium.webdrivers.trio_threads.base.actions import ActionsMixin
from osn_selenium.webdrivers.trio_threads.base.capture import CaptureMixin
from osn_selenium.webdrivers.trio_threads.base.element import ElementMixin
from osn_selenium.webdrivers.trio_threads.base.storage import StorageMixin
from osn_selenium.webdrivers.trio_threads.base.devtools import DevToolsMixin
from osn_selenium.webdrivers.trio_threads.base.lifecycle import LifecycleMixin
from osn_selenium.webdrivers.trio_threads.base.comonents import ComponentsMixin
from osn_selenium.webdrivers.trio_threads.base.navigation import NavigationMixin


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
			devtools_settings: Optional[DevToolsSettings] = None,
			capacity_limiter: Optional[trio.CapacityLimiter] = None,
	) -> None:
		super().__init__(
				webdriver_path=webdriver_path,
				flags_manager_type=flags_manager_type,
				flags=flags,
				implicitly_wait=implicitly_wait,
				page_load_timeout=page_load_timeout,
				script_timeout=script_timeout,
				window_rect=window_rect,
				capacity_limiter=capacity_limiter,
		)
		
		self._dev_tools = DevTools(parent_webdriver=self, devtools_settings=devtools_settings)
		
		self._js_executor = JSExecutor(execute_function=self.execute_script)
		
		self._cdp_executor = CDPExecutor(execute_function=self.execute_cdp_cmd)
	
	@property
	def cdp(self) -> CDPExecutor:
		return self._cdp_executor
	
	@property
	def dev_tools(self) -> DevTools:
		return self._dev_tools
	
	@property
	def javascript(self) -> JSExecutor:
		return self._js_executor
