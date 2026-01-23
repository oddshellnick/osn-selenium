from typing import Any, Dict
from osn_selenium.webdrivers.unified.blink.network import (
	UnifiedBlinkNetworkMixin
)
from osn_selenium.abstract.webdriver.blink.network import (
	AbstractBlinkNetworkMixin
)


__all__ = ["BlinkNetworkMixin"]


class BlinkNetworkMixin(UnifiedBlinkNetworkMixin, AbstractBlinkNetworkMixin):
	"""
	Mixin for network interception and condition simulation for Blink WebDrivers.

	Facilitates monitoring of network traffic, modifying requests/responses,
	and emulating specific network conditions like offline mode or latency.
	"""
	
	def delete_network_conditions(self) -> None:
		self._delete_network_conditions_impl()
	
	def get_network_conditions(self) -> Dict[str, Any]:
		return self._get_network_conditions_impl()
	
	def set_network_conditions(self, **network_conditions: Any) -> None:
		self._set_network_conditions_impl(**network_conditions)
