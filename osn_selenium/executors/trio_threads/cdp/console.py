import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.console import (
	UnifiedConsoleCDPExecutor
)
from osn_selenium.abstract.executors.cdp.console import (
	AbstractConsoleCDPExecutor
)


__all__ = ["ConsoleCDPExecutor"]


class ConsoleCDPExecutor(UnifiedConsoleCDPExecutor, TrioThreadMixin, AbstractConsoleCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedConsoleCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear_messages(self) -> None:
		return await self.sync_to_trio(sync_function=self._clear_messages_impl)()
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
