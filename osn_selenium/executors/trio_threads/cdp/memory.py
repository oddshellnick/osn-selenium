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
from osn_selenium.executors.unified.cdp.memory import (
	UnifiedMemoryCDPExecutor
)
from osn_selenium.abstract.executors.cdp.memory import (
	AbstractMemoryCDPExecutor
)


__all__ = ["MemoryCDPExecutor"]


class MemoryCDPExecutor(UnifiedMemoryCDPExecutor, TrioThreadMixin, AbstractMemoryCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedMemoryCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def forcibly_purge_java_script_memory(self) -> None:
		return await self.sync_to_trio(sync_function=self._forcibly_purge_java_script_memory_impl)()
	
	async def get_all_time_sampling_profile(self) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_all_time_sampling_profile_impl)()
	
	async def get_browser_sampling_profile(self) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_browser_sampling_profile_impl)()
	
	async def get_dom_counters(self) -> Tuple[int, int, int]:
		return await self.sync_to_trio(sync_function=self._get_dom_counters_impl)()
	
	async def get_dom_counters_for_leak_detection(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_dom_counters_for_leak_detection_impl)()
	
	async def get_sampling_profile(self) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_sampling_profile_impl)()
	
	async def prepare_for_leak_detection(self) -> None:
		return await self.sync_to_trio(sync_function=self._prepare_for_leak_detection_impl)()
	
	async def set_pressure_notifications_suppressed(self, suppressed: bool) -> None:
		return await self.sync_to_trio(sync_function=self._set_pressure_notifications_suppressed_impl)(suppressed=suppressed)
	
	async def simulate_pressure_notification(self, level: str) -> None:
		return await self.sync_to_trio(sync_function=self._simulate_pressure_notification_impl)(level=level)
	
	async def start_sampling(
			self,
			sampling_interval: Optional[int] = None,
			suppress_randomness: Optional[bool] = None
	) -> None:
		return await self.sync_to_trio(sync_function=self._start_sampling_impl)(
				sampling_interval=sampling_interval,
				suppress_randomness=suppress_randomness
		)
	
	async def stop_sampling(self) -> None:
		return await self.sync_to_trio(sync_function=self._stop_sampling_impl)()
