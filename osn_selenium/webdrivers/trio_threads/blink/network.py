from typing import Any, Dict
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.trio_threads.blink.base import BlinkBaseMixin
from osn_selenium.abstract.webdriver.blink.network import (
	AbstractBlinkNetworkMixin
)


class BlinkNetworkMixin(BlinkBaseMixin, AbstractBlinkNetworkMixin):
	"""
	Mixin for network interception and condition simulation for Blink WebDrivers.

	Facilitates monitoring of network traffic, modifying requests/responses,
	and emulating specific network conditions like offline mode or latency.
	"""
	
	@requires_driver
	async def delete_network_conditions(self) -> None:
		return await self.sync_to_trio(sync_function=self.driver.delete_network_conditions)()
	
	@requires_driver
	async def get_network_conditions(self) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self.driver.get_network_conditions)()
	
	@requires_driver
	async def set_network_conditions(self, **network_conditions: Dict[str, Any]) -> None:
		return await self.sync_to_trio(sync_function=self.driver.set_network_conditions)(**network_conditions)
