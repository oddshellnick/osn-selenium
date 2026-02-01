from typing_extensions import deprecated
from contextlib import asynccontextmanager
from osn_selenium.trio_bidi.mixin import TrioBiDiMixin
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Tuple
)
from selenium.webdriver.remote.bidi_connection import BidiConnection
from selenium.webdriver.remote.websocket_connection import WebSocketConnection
from osn_selenium.webdrivers.unified.core.devtools import (
	UnifiedCoreDevToolsMixin
)
from osn_selenium.abstract.webdriver.core.devtools import (
	AbstractCoreDevToolsMixin
)
from osn_selenium.exceptions.experimental import (
	NotImplementedExperimentalFeatureError
)


__all__ = ["CoreDevToolsMixin"]


class CoreDevToolsMixin(UnifiedCoreDevToolsMixin, TrioBiDiMixin, AbstractCoreDevToolsMixin):
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
	
	@deprecated(
			"This method is currently not supported. It will raise 'NotImplementedExperimentalFeatureError' on call."
	)
	async def network(self):
		raise NotImplementedExperimentalFeatureError(name="CoreDevToolsMixin.network")
	
	async def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		return await self.sync_to_trio(sync_function=self._start_devtools_impl)()
