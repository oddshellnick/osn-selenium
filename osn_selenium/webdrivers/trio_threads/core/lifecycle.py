from types import TracebackType
from osn_selenium.models import WindowRect
from osn_selenium.flags.models.base import BrowserFlags
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	Any,
	Dict,
	Optional,
	Type,
	Union
)
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
	
	async def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.sync_to_trio(sync_function=self._start_webdriver_impl)(flags=flags, window_rect=window_rect)
	
	async def __aenter__(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		await self.start_webdriver(flags=flags, window_rect=window_rect)
	
	async def stop_webdriver(self) -> None:
		await self.sync_to_trio(sync_function=self._stop_webdriver_impl)()
	
	async def __aexit__(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType],
	) -> bool:
		"""
		Asynchronously exits the WebDriver context.

		Args:
			exc_type (Optional[Type[BaseException]]): The exception type, if any.
			exc_val (Optional[BaseException]): The exception value, if any.
			exc_tb (Optional[TracebackType]): The exception traceback, if any.

		Returns:
			bool: True if an exception was suppressed, False otherwise.
		"""
		
		await self.stop_webdriver()
		
		if exc_type is not None and exc_val is not None and exc_tb is not None:
			return True
		
		return False
	
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
	
	async def stop_client(self) -> None:
		await self.sync_to_trio(sync_function=self._stop_client_impl)()
