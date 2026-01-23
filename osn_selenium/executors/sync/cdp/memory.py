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


class MemoryCDPExecutor(UnifiedMemoryCDPExecutor, AbstractMemoryCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedMemoryCDPExecutor.__init__(self, execute_function=execute_function)
	
	def forcibly_purge_java_script_memory(self) -> None:
		return self._forcibly_purge_java_script_memory_impl()
	
	def get_all_time_sampling_profile(self) -> Dict[str, Any]:
		return self._get_all_time_sampling_profile_impl()
	
	def get_browser_sampling_profile(self) -> Dict[str, Any]:
		return self._get_browser_sampling_profile_impl()
	
	def get_dom_counters(self) -> Tuple[int, int, int]:
		return self._get_dom_counters_impl()
	
	def get_dom_counters_for_leak_detection(self) -> List[Dict[str, Any]]:
		return self._get_dom_counters_for_leak_detection_impl()
	
	def get_sampling_profile(self) -> Dict[str, Any]:
		return self._get_sampling_profile_impl()
	
	def prepare_for_leak_detection(self) -> None:
		return self._prepare_for_leak_detection_impl()
	
	def set_pressure_notifications_suppressed(self, suppressed: bool) -> None:
		return self._set_pressure_notifications_suppressed_impl(suppressed=suppressed)
	
	def simulate_pressure_notification(self, level: str) -> None:
		return self._simulate_pressure_notification_impl(level=level)
	
	def start_sampling(
			self,
			sampling_interval: Optional[int] = None,
			suppress_randomness: Optional[bool] = None
	) -> None:
		return self._start_sampling_impl(
				sampling_interval=sampling_interval,
				suppress_randomness=suppress_randomness
		)
	
	def stop_sampling(self) -> None:
		return self._stop_sampling_impl()
