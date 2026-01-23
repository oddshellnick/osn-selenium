import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.performance import (
	UnifiedPerformanceCDPExecutor
)
from osn_selenium.abstract.executors.cdp.performance import (
	AbstractPerformanceCDPExecutor
)


__all__ = ["PerformanceCDPExecutor"]


class PerformanceCDPExecutor(
		UnifiedPerformanceCDPExecutor,
		TrioThreadMixin,
		AbstractPerformanceCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedPerformanceCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self, time_domain: Optional[str] = None) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)(time_domain=time_domain)
	
	async def get_metrics(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_metrics_impl)()
	
	async def set_time_domain(self, time_domain: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_time_domain_impl)(time_domain=time_domain)
