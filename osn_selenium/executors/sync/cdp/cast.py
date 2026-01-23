from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.executors.unified.cdp.cast import (
	UnifiedCastCDPExecutor
)
from osn_selenium.abstract.executors.cdp.cast import (
	AbstractCastCDPExecutor
)


__all__ = ["CastCDPExecutor"]


class CastCDPExecutor(UnifiedCastCDPExecutor, AbstractCastCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedCastCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self, presentation_url: Optional[str] = None) -> None:
		return self._enable_impl(presentation_url=presentation_url)
	
	def set_sink_to_use(self, sink_name: str) -> None:
		return self._set_sink_to_use_impl(sink_name=sink_name)
	
	def start_desktop_mirroring(self, sink_name: str) -> None:
		return self._start_desktop_mirroring_impl(sink_name=sink_name)
	
	def start_tab_mirroring(self, sink_name: str) -> None:
		return self._start_tab_mirroring_impl(sink_name=sink_name)
	
	def stop_casting(self, sink_name: str) -> None:
		return self._stop_casting_impl(sink_name=sink_name)
