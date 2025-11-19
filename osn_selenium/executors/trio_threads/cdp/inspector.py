import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.inspector import (
	UnifiedInspectorCDPExecutor
)
from osn_selenium.abstract.executors.cdp.inspector import (
	AbstractInspectorCDPExecutor
)


__all__ = ["InspectorCDPExecutor"]


class InspectorCDPExecutor(
		UnifiedInspectorCDPExecutor,
		TrioThreadMixin,
		AbstractInspectorCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedInspectorCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
