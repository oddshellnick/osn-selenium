from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.background_service import (
	AbstractBackgroundServiceCDPExecutor
)


class BackgroundServiceCDPExecutor(AbstractBackgroundServiceCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def clear_events(self, service: str) -> None:
		return await self._execute_function("BackgroundService.clearEvents", locals())
	
	async def set_recording(self, should_record: bool, service: str) -> None:
		return await self._execute_function("BackgroundService.setRecording", locals())
	
	async def start_observing(self, service: str) -> None:
		return await self._execute_function("BackgroundService.startObserving", locals())
	
	async def stop_observing(self, service: str) -> None:
		return await self._execute_function("BackgroundService.stopObserving", locals())
