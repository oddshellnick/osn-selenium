import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.tethering import (
	UnifiedTetheringCDPExecutor
)
from osn_selenium.abstract.executors.cdp.tethering import (
	AbstractTetheringCDPExecutor
)


__all__ = ["TetheringCDPExecutor"]


class TetheringCDPExecutor(
		UnifiedTetheringCDPExecutor,
		TrioThreadMixin,
		AbstractTetheringCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedTetheringCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def bind(self, port: int) -> None:
		return await self.sync_to_trio(sync_function=self._bind_impl)(port=port)
	
	async def unbind(self, port: int) -> None:
		return await self.sync_to_trio(sync_function=self._unbind_impl)(port=port)
