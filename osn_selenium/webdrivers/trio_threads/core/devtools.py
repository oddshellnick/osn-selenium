from contextlib import asynccontextmanager
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Tuple
)
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.trio_threads.network import Network
from osn_selenium.webdrivers._functions import build_cdp_kwargs
from selenium.webdriver.remote.bidi_connection import BidiConnection
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
from osn_selenium.abstract.webdriver.core.devtools import (
	AbstractCoreDevToolsMixin
)


class CoreDevToolsMixin(CoreBaseMixin, AbstractCoreDevToolsMixin):
	"""
	Mixin for Chrome DevTools Protocol (CDP) and BiDi interactions in Core WebDrivers.

	Facilitates low-level browser control via CDP commands, network interception,
	and bidirectional communication sessions.
	"""
	
	@asynccontextmanager
	@requires_driver
	async def bidi_connection(self) -> AsyncGenerator[BidiConnection, Any]:
		async with self.driver.bidi_connection() as bidi_connection:
			yield bidi_connection
	
	@requires_driver
	async def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return await self._sync_to_trio(
				self.driver.execute_cdp_cmd,
				cmd=cmd,
				cmd_args=build_cdp_kwargs(**cmd_args)
		)
	
	@requires_driver
	async def network(self) -> Network:
		legacy = await self._sync_to_trio(lambda: self.driver.network)
		
		return Network(
				selenium_network=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	@requires_driver
	async def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		return await self._sync_to_trio(self.driver.start_devtools)
