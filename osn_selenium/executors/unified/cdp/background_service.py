from typing import Any, Callable, Dict


__all__ = ["UnifiedBackgroundServiceCDPExecutor"]


class UnifiedBackgroundServiceCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_events_impl(self, service: str) -> None:
		return self._execute_function("BackgroundService.clearEvents", {"service": service})
	
	def _set_recording_impl(self, should_record: bool, service: str) -> None:
		return self._execute_function(
				"BackgroundService.setRecording",
				{"should_record": should_record, "service": service}
		)
	
	def _start_observing_impl(self, service: str) -> None:
		return self._execute_function("BackgroundService.startObserving", {"service": service})
	
	def _stop_observing_impl(self, service: str) -> None:
		return self._execute_function("BackgroundService.stopObserving", {"service": service})
