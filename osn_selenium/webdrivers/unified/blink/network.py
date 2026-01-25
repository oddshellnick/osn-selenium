from typing import Any, Dict
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)


__all__ = ["UnifiedBlinkNetworkMixin"]


class UnifiedBlinkNetworkMixin(UnifiedBlinkBaseMixin):
	@requires_driver
	def _delete_network_conditions_impl(self) -> None:
		self._driver_impl.delete_network_conditions()
	
	@requires_driver
	def _get_network_conditions_impl(self) -> Dict[str, Any]:
		return self._driver_impl.get_network_conditions()
	
	@requires_driver
	def _set_network_conditions_impl(self, **network_conditions: Any) -> None:
		self._driver_impl.set_network_conditions(**network_conditions)
