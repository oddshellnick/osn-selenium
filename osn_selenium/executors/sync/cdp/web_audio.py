from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.web_audio import (
	UnifiedWebAudioCDPExecutor
)
from osn_selenium.abstract.executors.cdp.web_audio import (
	AbstractWebAudioCDPExecutor
)


__all__ = ["WebAudioCDPExecutor"]


class WebAudioCDPExecutor(UnifiedWebAudioCDPExecutor, AbstractWebAudioCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedWebAudioCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
	
	def get_realtime_data(self, context_id: str) -> Dict[str, Any]:
		return self._get_realtime_data_impl(context_id=context_id)
