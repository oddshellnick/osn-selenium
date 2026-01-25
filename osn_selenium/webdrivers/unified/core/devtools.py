from contextlib import asynccontextmanager
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Tuple
)
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers._args_helpers import build_cdp_kwargs
from selenium.webdriver.remote.bidi_connection import BidiConnection
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin
from selenium.webdriver.remote.websocket_connection import WebSocketConnection


__all__ = ["UnifiedCoreDevToolsMixin"]


class UnifiedCoreDevToolsMixin(UnifiedCoreBaseMixin):
	@asynccontextmanager
	@requires_driver
	async def _bidi_connection_impl(self) -> AsyncGenerator[BidiConnection, Any]:
		async with self._driver_impl.bidi_connection() as bidi_connection:
			yield bidi_connection
	
	@requires_driver
	def _execute_cdp_cmd_impl(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		return self._driver_impl.execute_cdp_cmd(cmd=cmd, cmd_args=build_cdp_kwargs(**cmd_args))
	
	@requires_driver
	def _network_impl(self) -> Any:
		return self._driver_impl.network
	
	@requires_driver
	def _start_devtools_impl(self) -> Tuple[Any, WebSocketConnection]:
		return self._driver_impl.start_devtools()
