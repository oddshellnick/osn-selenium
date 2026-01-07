from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.backgroundservice import (
	AbstractBackgroundServiceCDPExecutor
)


class BackgroundServiceCDPExecutor(AbstractBackgroundServiceCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear_events(self, service: str) -> None:
		return self._execute_function("BackgroundService.clearEvents", locals())
	
	def set_recording(self, should_record: bool, service: str) -> None:
		return self._execute_function("BackgroundService.setRecording", locals())
	
	def start_observing(self, service: str) -> None:
		return self._execute_function("BackgroundService.startObserving", locals())
	
	def stop_observing(self, service: str) -> None:
		return self._execute_function("BackgroundService.stopObserving", locals())
