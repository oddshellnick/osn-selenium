from typing import (
	Any,
	Callable,
	Dict,
	Optional
)


__all__ = ["UnifiedCastCDPExecutor"]


class UnifiedCastCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Cast.disable", {})
	
	def _enable_impl(self, presentation_url: Optional[str] = None) -> None:
		return self._execute_function("Cast.enable", {"presentation_url": presentation_url})
	
	def _set_sink_to_use_impl(self, sink_name: str) -> None:
		return self._execute_function("Cast.setSinkToUse", {"sink_name": sink_name})
	
	def _start_desktop_mirroring_impl(self, sink_name: str) -> None:
		return self._execute_function("Cast.startDesktopMirroring", {"sink_name": sink_name})
	
	def _start_tab_mirroring_impl(self, sink_name: str) -> None:
		return self._execute_function("Cast.startTabMirroring", {"sink_name": sink_name})
	
	def _stop_casting_impl(self, sink_name: str) -> None:
		return self._execute_function("Cast.stopCasting", {"sink_name": sink_name})
