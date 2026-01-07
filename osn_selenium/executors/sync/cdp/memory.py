from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)
from osn_selenium.abstract.executors.cdp.memory import (
	AbstractMemoryCDPExecutor
)


class MemoryCDPExecutor(AbstractMemoryCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def forcibly_purge_java_script_memory(self) -> None:
		return self._execute_function("Memory.forciblyPurgeJavaScriptMemory", locals())
	
	def get_all_time_sampling_profile(self) -> List[Any]:
		return self._execute_function("Memory.getAllTimeSamplingProfile", locals())
	
	def get_browser_sampling_profile(self) -> List[Any]:
		return self._execute_function("Memory.getBrowserSamplingProfile", locals())
	
	def get_dom_counters(self) -> Tuple[int]:
		return self._execute_function("Memory.getDOMCounters", locals())
	
	def get_dom_counters_for_leak_detection(self) -> List[Any]:
		return self._execute_function("Memory.getDOMCountersForLeakDetection", locals())
	
	def get_sampling_profile(self) -> List[Any]:
		return self._execute_function("Memory.getSamplingProfile", locals())
	
	def prepare_for_leak_detection(self) -> None:
		return self._execute_function("Memory.prepareForLeakDetection", locals())
	
	def set_pressure_notifications_suppressed(self, suppressed: bool) -> None:
		return self._execute_function("Memory.setPressureNotificationsSuppressed", locals())
	
	def simulate_pressure_notification(self, level: str) -> None:
		return self._execute_function("Memory.simulatePressureNotification", locals())
	
	def start_sampling(
			self,
			sampling_interval: Optional[int] = None,
			suppress_randomness: Optional[bool] = None
	) -> None:
		return self._execute_function("Memory.startSampling", locals())
	
	def stop_sampling(self) -> None:
		return self._execute_function("Memory.stopSampling", locals())
