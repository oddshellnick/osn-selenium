from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.background_service import (
	UnifiedBackgroundServiceCDPExecutor
)
from osn_selenium.abstract.executors.cdp.background_service import (
	AbstractBackgroundServiceCDPExecutor
)


__all__ = ["BackgroundServiceCDPExecutor"]


class BackgroundServiceCDPExecutor(
		UnifiedBackgroundServiceCDPExecutor,
		AbstractBackgroundServiceCDPExecutor
):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedBackgroundServiceCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear_events(self, service: str) -> None:
		return self._clear_events_impl(service=service)
	
	def set_recording(self, should_record: bool, service: str) -> None:
		return self._set_recording_impl(should_record=should_record, service=service)
	
	def start_observing(self, service: str) -> None:
		return self._start_observing_impl(service=service)
	
	def stop_observing(self, service: str) -> None:
		return self._stop_observing_impl(service=service)
