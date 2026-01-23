from typing import Any, Dict, List
from osn_selenium.webdrivers.unified.blink.casting import (
	UnifiedBlinkCastingMixin
)
from osn_selenium.abstract.webdriver.blink.casting import (
	AbstractBlinkCastingMixin
)


__all__ = ["BlinkCastingMixin"]


class BlinkCastingMixin(UnifiedBlinkCastingMixin, AbstractBlinkCastingMixin):
	"""
	Mixin handling object type casting and wrapping for Blink WebDrivers.

	Ensures that raw Selenium objects are converted into their corresponding
	internal wrapper representations and vice versa during method calls.
	"""
	
	def get_sinks(self) -> List[Dict[str, Any]]:
		return self._get_sinks_impl()
	
	def set_sink_to_use(self, sink_name: str) -> Dict[str, Any]:
		return self._set_sink_to_use_impl(sink_name=sink_name)
	
	def start_desktop_mirroring(self, sink_name: str) -> Dict[str, Any]:
		return self._start_desktop_mirroring_impl(sink_name=sink_name)
	
	def start_tab_mirroring(self, sink_name: str) -> Dict[str, Any]:
		return self._start_tab_mirroring_impl(sink_name=sink_name)
	
	def stop_casting(self, sink_name: str) -> Dict[str, Any]:
		return self._stop_casting_impl(sink_name=sink_name)
