from typing import Any, Dict
from osn_selenium.trio_threads_mixin import TrioThreadMixin
from osn_selenium.webdrivers.unified.blink.network import (
	UnifiedBlinkNetworkMixin
)
from osn_selenium.abstract.webdriver.blink.network import (
	AbstractBlinkNetworkMixin
)


__all__ = ["BlinkNetworkMixin"]


class BlinkNetworkMixin(UnifiedBlinkNetworkMixin, TrioThreadMixin, AbstractBlinkNetworkMixin):
	"""
	Mixin for network interception and condition simulation for Blink WebDrivers.

	Facilitates monitoring of network traffic, modifying requests/responses,
	and emulating specific network conditions like offline mode or latency.
	"""
	
	async def delete_network_conditions(self) -> None:
		await self.sync_to_trio(sync_function=self._delete_network_conditions_impl)()
	
	async def get_network_conditions(self) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_network_conditions_impl)()
	
	async def set_network_conditions(self, **network_conditions: Any) -> None:
		await self.sync_to_trio(sync_function=self._set_network_conditions_impl)(**network_conditions)
