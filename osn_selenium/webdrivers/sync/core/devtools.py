from contextlib import asynccontextmanager
from osn_selenium.instances.sync.network import Network
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Tuple
)
from selenium.webdriver.remote.bidi_connection import BidiConnection
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
from osn_selenium.webdrivers.unified.core.devtools import (
	UnifiedCoreDevToolsMixin
)
from osn_selenium.abstract.webdriver.core.devtools import (
	AbstractCoreDevToolsMixin
)


__all__ = ["CoreDevToolsMixin"]


class CoreDevToolsMixin(UnifiedCoreDevToolsMixin, AbstractCoreDevToolsMixin):
	"""
	Mixin for Chrome DevTools Protocol (CDP) and BiDi interactions in Core WebDrivers.

	Facilitates low-level browser control via CDP commands, network interception,
	and bidirectional communication sessions.
	"""
	
	@asynccontextmanager
	async def bidi_connection(self) -> AsyncGenerator[BidiConnection, Any]:
		async with self._bidi_connection_impl() as bidi:
			yield bidi
	
	def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return self._execute_cdp_cmd_impl(cmd=cmd, cmd_args=cmd_args)
	
	def network(self) -> Network:
		legacy = self._network_impl()
		
		return get_sync_instance_wrapper(wrapper_class=Network, legacy_object=legacy)
	
	def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		return self._start_devtools_impl()
