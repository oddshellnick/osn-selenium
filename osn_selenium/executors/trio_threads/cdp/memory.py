from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.memory import (
	AbstractMemoryCDPExecutor
)


class MemoryCDPExecutor(AbstractMemoryCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def forcibly_purge_java_script_memory(self) -> None:
		return await self._execute_function("Memory.forciblyPurgeJavaScriptMemory", locals())
	
	async def get_all_time_sampling_profile(self) -> List[Any]:
		return await self._execute_function("Memory.getAllTimeSamplingProfile", locals())
	
	async def get_browser_sampling_profile(self) -> List[Any]:
		return await self._execute_function("Memory.getBrowserSamplingProfile", locals())
	
	async def get_dom_counters(self) -> Tuple[int]:
		return await self._execute_function("Memory.getDOMCounters", locals())
	
	async def get_dom_counters_for_leak_detection(self) -> List[Any]:
		return await self._execute_function("Memory.getDOMCountersForLeakDetection", locals())
	
	async def get_sampling_profile(self) -> List[Any]:
		return await self._execute_function("Memory.getSamplingProfile", locals())
	
	async def prepare_for_leak_detection(self) -> None:
		return await self._execute_function("Memory.prepareForLeakDetection", locals())
	
	async def set_pressure_notifications_suppressed(self, suppressed: bool) -> None:
		return await self._execute_function("Memory.setPressureNotificationsSuppressed", locals())
	
	async def simulate_pressure_notification(self, level: str) -> None:
		return await self._execute_function("Memory.simulatePressureNotification", locals())
	
	async def start_sampling(
			self,
			sampling_interval: Optional[int] = None,
			suppress_randomness: Optional[bool] = None
	) -> None:
		return await self._execute_function("Memory.startSampling", locals())
	
	async def stop_sampling(self) -> None:
		return await self._execute_function("Memory.stopSampling", locals())
