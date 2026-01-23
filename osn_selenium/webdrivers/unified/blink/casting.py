from typing import Any, Dict, List
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)


__all__ = ["UnifiedBlinkCastingMixin"]


class UnifiedBlinkCastingMixin(UnifiedBlinkBaseMixin):
	@requires_driver
	def _get_sinks_impl(self) -> List[Dict[str, Any]]:
		return self._driver_impl.get_sinks()
	
	@requires_driver
	def _set_sink_to_use_impl(self, sink_name: str) -> Dict[str, Any]:
		return self._driver_impl.set_sink_to_use(sink_name=sink_name)
	
	@requires_driver
	def _start_desktop_mirroring_impl(self, sink_name: str) -> Dict[str, Any]:
		return self._driver_impl.start_desktop_mirroring(sink_name=sink_name)
	
	@requires_driver
	def _start_tab_mirroring_impl(self, sink_name: str) -> Dict[str, Any]:
		return self._driver_impl.start_tab_mirroring(sink_name=sink_name)
	
	@requires_driver
	def _stop_casting_impl(self, sink_name: str) -> Dict[str, Any]:
		return self._driver_impl.stop_casting(sink_name=sink_name)
