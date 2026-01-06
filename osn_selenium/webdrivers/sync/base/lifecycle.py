from osn_selenium.types import WindowRect
from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.base.settings import SettingsMixin
from osn_selenium.webdrivers.sync.base.timeouts import TimeoutsMixin
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from osn_selenium.abstract.webdriver.base.lifecycle import (
	AbstractLifecycleMixin
)


class LifecycleMixin(SettingsMixin, TimeoutsMixin, AbstractLifecycleMixin):
	def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]) -> None:
		self._driver = legacyWebDriver(
				command_executor=command_executor,
				options=self._webdriver_flags_manager.options,
		)
		
		self.set_driver_timeouts(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_script_timeout,
		)
		
		self._is_active = True
	
	def _create_driver(self):
		raise NotImplementedError("This function must be implemented in child classes.")
	
	def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if self.driver is None:
			self.update_settings(flags=flags, window_rect=window_rect)
		
			self._create_driver()
	
	@requires_driver
	def quit(self) -> None:
		self.driver.quit()
	
	@requires_driver
	def close_webdriver(self) -> None:
		if self.driver is not None:
			self.quit()
			self._driver = None
	
	def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		self.close_webdriver()
		self.start_webdriver(flags=flags, window_rect=window_rect)
	
	@requires_driver
	def start_client(self) -> None:
		self.driver.start_client()
	
	@requires_driver
	def start_session(self, capabilities: Dict[str, Any]) -> None:
		self.driver.start_session(capabilities=capabilities)
	
	@requires_driver
	def stop_client(self) -> None:
		self.driver.stop_client()
