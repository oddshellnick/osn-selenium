from contextlib import asynccontextmanager
from osn_selenium.instances.sync.network import Network
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Tuple
)
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers._functions import build_cdp_kwargs
from selenium.webdriver.remote.bidi_connection import BidiConnection
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
from osn_selenium.abstract.webdriver.core.devtools import (
	AbstractCoreDevToolsMixin
)


class CoreDevToolsMixin(CoreBaseMixin, AbstractCoreDevToolsMixin):
	@asynccontextmanager
	@requires_driver
	async def bidi_connection(self) -> AsyncGenerator[BidiConnection, Any]:
		async with self.driver.bidi_connection() as bidi_connection:
			yield bidi_connection
	
	@requires_driver
	def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return self.driver.execute_cdp_cmd(cmd=cmd, cmd_args=build_cdp_kwargs(**cmd_args))
	
	@requires_driver
	def network(self) -> Network:
		legacy = self.driver.network
		
		return Network(selenium_network=legacy)
	
	@requires_driver
	def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		return self.driver.start_devtools()
