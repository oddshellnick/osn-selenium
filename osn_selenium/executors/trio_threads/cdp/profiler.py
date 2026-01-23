import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.profiler import (
	UnifiedProfilerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.profiler import (
	AbstractProfilerCDPExecutor
)


__all__ = ["ProfilerCDPExecutor"]


class ProfilerCDPExecutor(
		UnifiedProfilerCDPExecutor,
		TrioThreadMixin,
		AbstractProfilerCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedProfilerCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def get_best_effort_coverage(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_best_effort_coverage_impl)()
	
	async def set_sampling_interval(self, interval: int) -> None:
		return await self.sync_to_trio(sync_function=self._set_sampling_interval_impl)(interval=interval)
	
	async def start(self) -> None:
		return await self.sync_to_trio(sync_function=self._start_impl)()
	
	async def start_precise_coverage(
			self,
			call_count: Optional[bool] = None,
			detailed: Optional[bool] = None,
			allow_triggered_updates: Optional[bool] = None
	) -> float:
		return await self.sync_to_trio(sync_function=self._start_precise_coverage_impl)(
				call_count=call_count,
				detailed=detailed,
				allow_triggered_updates=allow_triggered_updates
		)
	
	async def stop(self) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._stop_impl)()
	
	async def stop_precise_coverage(self) -> None:
		return await self.sync_to_trio(sync_function=self._stop_precise_coverage_impl)()
	
	async def take_precise_coverage(self) -> Tuple[List[Dict[str, Any]], float]:
		return await self.sync_to_trio(sync_function=self._take_precise_coverage_impl)()
