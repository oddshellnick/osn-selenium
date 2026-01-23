from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["UnifiedMemoryCDPExecutor"]


class UnifiedMemoryCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _forcibly_purge_java_script_memory_impl(self) -> None:
		return self._execute_function("Memory.forciblyPurgeJavaScriptMemory", {})
	
	def _get_all_time_sampling_profile_impl(self) -> Dict[str, Any]:
		return self._execute_function("Memory.getAllTimeSamplingProfile", {})
	
	def _get_browser_sampling_profile_impl(self) -> Dict[str, Any]:
		return self._execute_function("Memory.getBrowserSamplingProfile", {})
	
	def _get_dom_counters_for_leak_detection_impl(self) -> List[Dict[str, Any]]:
		return self._execute_function("Memory.getDOMCountersForLeakDetection", {})
	
	def _get_dom_counters_impl(self) -> Tuple[int, int, int]:
		return self._execute_function("Memory.getDOMCounters", {})
	
	def _get_sampling_profile_impl(self) -> Dict[str, Any]:
		return self._execute_function("Memory.getSamplingProfile", {})
	
	def _prepare_for_leak_detection_impl(self) -> None:
		return self._execute_function("Memory.prepareForLeakDetection", {})
	
	def _set_pressure_notifications_suppressed_impl(self, suppressed: bool) -> None:
		return self._execute_function("Memory.setPressureNotificationsSuppressed", {"suppressed": suppressed})
	
	def _simulate_pressure_notification_impl(self, level: str) -> None:
		return self._execute_function("Memory.simulatePressureNotification", {"level": level})
	
	def _start_sampling_impl(
			self,
			sampling_interval: Optional[int] = None,
			suppress_randomness: Optional[bool] = None
	) -> None:
		return self._execute_function(
				"Memory.startSampling",
				{
					"sampling_interval": sampling_interval,
					"suppress_randomness": suppress_randomness
				}
		)
	
	def _stop_sampling_impl(self) -> None:
		return self._execute_function("Memory.stopSampling", {})
