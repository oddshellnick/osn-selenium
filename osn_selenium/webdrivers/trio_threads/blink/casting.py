from typing import Any, Dict, List
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink.casting import (
	AbstractBlinkCastingMixin
)


class BlinkCastingMixin(BlinkBaseMixin, AbstractBlinkCastingMixin):
	"""
	Mixin handling object type casting and wrapping for Blink WebDrivers.

	Ensures that raw Selenium objects are converted into their corresponding
	internal wrapper representations and vice versa during method calls.
	"""
	
	@requires_driver
	async def get_sinks(self) -> List[Dict[str, Any]]:
		return await self._wrap_to_trio(self.driver.get_sinks)
	
	@requires_driver
	async def set_sink_to_use(self, sink_name: str) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.set_sink_to_use, sink_name=sink_name)
	
	@requires_driver
	async def start_desktop_mirroring(self, sink_name: str) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.start_desktop_mirroring, sink_name=sink_name)
	
	@requires_driver
	async def start_tab_mirroring(self, sink_name: str) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.start_tab_mirroring, sink_name=sink_name)
	
	@requires_driver
	async def stop_casting(self, sink_name: str) -> Dict[str, Any]:
		return await self._wrap_to_trio(self.driver.stop_casting, sink_name=sink_name)
