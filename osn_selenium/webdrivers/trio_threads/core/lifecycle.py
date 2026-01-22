from osn_selenium.types import WindowRect
from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.webdrivers.decorators import requires_driver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.webdrivers.trio_threads.core.settings import CoreSettingsMixin
from osn_selenium.webdrivers.trio_threads.core.timeouts import CoreTimeoutsMixin
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)
from osn_selenium.abstract.webdriver.core.lifecycle import (
	AbstractCoreLifecycleMixin
)


class CoreLifecycleMixin(CoreSettingsMixin, CoreTimeoutsMixin, AbstractCoreLifecycleMixin):
	"""
	Mixin for managing the lifecycle of the Core WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	async def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]) -> None:
		def _make() -> legacyWebDriver:
			return legacyWebDriver(
					command_executor=command_executor,
					options=self._webdriver_flags_manager.options,
			)
		
		self._driver = await self.sync_to_trio(sync_function=_make)()
		
		await self.set_driver_timeouts(
				page_load_timeout=self._base_page_load_timeout,
				implicit_wait_timeout=self._base_implicitly_wait,
				script_timeout=self._base_script_timeout,
		)
		
		self._is_active = True
	
	async def _create_driver(self):
		raise NotImplementedError("This function must be implemented in child classes.")
	
	async def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		if self.driver is None:
			await self.update_settings(flags=flags, window_rect=window_rect)
		
			await self._create_driver()
	
	@requires_driver
	async def quit(self) -> None:
		await self.sync_to_trio(sync_function=self.driver.quit)()
	
	@requires_driver
	async def close_webdriver(self) -> None:
		if self.driver is not None:
			await self.quit()
			self._driver = None
	
	async def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.close_webdriver()
		await self.start_webdriver(flags=flags, window_rect=window_rect)
	
	@requires_driver
	async def start_client(self) -> None:
		await self.sync_to_trio(sync_function=self.driver.start_client)()
	
	@requires_driver
	async def start_session(self, capabilities: Dict[str, Any]) -> None:
		await self.sync_to_trio(sync_function=self.driver.start_session)(capabilities=capabilities)
	
	@requires_driver
	async def stop_client(self) -> None:
		await self.sync_to_trio(sync_function=self.driver.stop_client)()
