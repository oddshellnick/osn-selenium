from typing import Any, Dict, List
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.webdrivers.unified.blink.casting import (
	UnifiedBlinkCastingMixin
)
from osn_selenium.abstract.webdriver.blink.casting import (
	AbstractBlinkCastingMixin
)


__all__ = ["BlinkCastingMixin"]


class BlinkCastingMixin(UnifiedBlinkCastingMixin, TrioThreadMixin, AbstractBlinkCastingMixin):
	"""
	Mixin handling object type casting and wrapping for Blink WebDrivers.

	Ensures that raw Selenium objects are converted into their corresponding
	internal wrapper representations and vice versa during method calls.
	"""
	
	async def get_sinks(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_sinks_impl)()
	
	async def set_sink_to_use(self, sink_name: str) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._set_sink_to_use_impl)(sink_name=sink_name)
	
	async def start_desktop_mirroring(self, sink_name: str) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._start_desktop_mirroring_impl)(sink_name=sink_name)
	
	async def start_tab_mirroring(self, sink_name: str) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._start_tab_mirroring_impl)(sink_name=sink_name)
	
	async def stop_casting(self, sink_name: str) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._stop_casting_impl)(sink_name=sink_name)
