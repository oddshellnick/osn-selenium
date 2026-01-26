from osn_selenium.models import WindowRect
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from osn_selenium.flags.models.base import BrowserFlags
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.webdrivers.unified.core.lifecycle import (
	UnifiedCoreLifecycleMixin
)
from osn_selenium.abstract.webdriver.core.lifecycle import (
	AbstractCoreLifecycleMixin
)


__all__ = ["CoreLifecycleMixin"]


class CoreLifecycleMixin(UnifiedCoreLifecycleMixin, TrioThreadMixin, AbstractCoreLifecycleMixin):
	"""
	Mixin for managing the lifecycle of the Core WebDriver.

	Handles the creation, startup, shutdown, and restarting processes of the
	underlying browser instance, ensuring clean session management.
	"""
	
	async def close_webdriver(self) -> None:
		await self.sync_to_trio(sync_function=self._close_webdriver_impl)()
	
	async def quit(self) -> None:
		await self.sync_to_trio(sync_function=self._quit_impl)()
	
	async def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]) -> None:
		await self.sync_to_trio(sync_function=self._remote_connect_driver_impl)(command_executor=command_executor)
	
	async def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._restart_webdriver_impl)(flags=flags, window_rect=window_rect)
	
	async def start_client(self) -> None:
		await self.sync_to_trio(sync_function=self._start_client_impl)()
	
	async def start_session(self, capabilities: Dict[str, Any]) -> None:
		await self.sync_to_trio(sync_function=self._start_session_impl)(capabilities=capabilities)
	
	async def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._start_webdriver_impl)(flags=flags, window_rect=window_rect)
	
	async def stop_client(self) -> None:
		await self.sync_to_trio(sync_function=self._stop_client_impl)()
