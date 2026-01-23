from typing import Any, Callable, Dict


__all__ = ["UnifiedWebAudioCDPExecutor"]


class UnifiedWebAudioCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("WebAudio.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("WebAudio.enable", {})
	
	def _get_realtime_data_impl(self, context_id: str) -> Dict[str, Any]:
		return self._execute_function("WebAudio.getRealtimeData", {"context_id": context_id})
