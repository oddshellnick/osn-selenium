import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.log import (
	UnifiedLogCDPExecutor
)
from osn_selenium.abstract.executors.cdp.log import (
	AbstractLogCDPExecutor
)


__all__ = ["LogCDPExecutor"]


class LogCDPExecutor(UnifiedLogCDPExecutor, TrioThreadMixin, AbstractLogCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedLogCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear(self) -> None:
		return await self.sync_to_trio(sync_function=self._clear_impl)()
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def start_violations_report(self, config: List[Dict[str, Any]]) -> None:
		return await self.sync_to_trio(sync_function=self._start_violations_report_impl)(config=config)
	
	async def stop_violations_report(self) -> None:
		return await self.sync_to_trio(sync_function=self._stop_violations_report_impl)()
