import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List
)
from osn_selenium.executors.unified.cdp.performance_timeline import (
	UnifiedPerformanceTimelineCDPExecutor
)
from osn_selenium.abstract.executors.cdp.performance_timeline import (
	AbstractPerformanceTimelineCDPExecutor
)


class PerformanceTimelineCDPExecutor(
		UnifiedPerformanceTimelineCDPExecutor,
		TrioThreadMixin,
		AbstractPerformanceTimelineCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedPerformanceTimelineCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def enable(self, event_types: List[str]) -> None:
		return await self._sync_to_trio(self._enable_impl, event_types=event_types)
