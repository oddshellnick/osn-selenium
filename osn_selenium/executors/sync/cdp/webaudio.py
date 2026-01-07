from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.webaudio import (
	AbstractWebAudioCDPExecutor
)


class WebAudioCDPExecutor(AbstractWebAudioCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("WebAudio.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("WebAudio.enable", locals())
	
	def get_realtime_data(self, context_id: str) -> Any:
		return self._execute_function("WebAudio.getRealtimeData", locals())
