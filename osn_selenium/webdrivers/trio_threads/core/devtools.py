from contextlib import asynccontextmanager
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Tuple
)
from osn_selenium.instances.trio_threads.network import Network
from selenium.webdriver.remote.bidi_connection import BidiConnection
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.devtools import (
	UnifiedCoreDevToolsMixin
)
from osn_selenium.abstract.webdriver.core.devtools import (
	AbstractCoreDevToolsMixin
)


__all__ = ["CoreDevToolsMixin"]


class CoreDevToolsMixin(UnifiedCoreDevToolsMixin, TrioThreadMixin, AbstractCoreDevToolsMixin):
	"""
	Mixin for Chrome DevTools Protocol (CDP) and BiDi interactions in Core WebDrivers.

	Facilitates low-level browser control via CDP commands, network interception,
	and bidirectional communication sessions.
	"""
	
	@asynccontextmanager
	async def bidi_connection(self) -> AsyncGenerator[BidiConnection, Any]:
		async with self._bidi_connection_impl() as bidi:
			yield bidi
	
	async def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return await self.sync_to_trio(sync_function=self._execute_cdp_cmd_impl)(cmd=cmd, cmd_args=cmd_args)
	
	async def network(self) -> Network:
		legacy = await self.sync_to_trio(sync_function=self._network_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Network,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		return await self.sync_to_trio(sync_function=self._start_devtools_impl)()
