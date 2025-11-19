from typing import Any
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)


__all__ = ["UnifiedBlinkLoggingMixin"]


class UnifiedBlinkLoggingMixin(UnifiedBlinkBaseMixin):
	@requires_driver
	def _get_log_impl(self, log_type: str) -> Any:
		return self._driver_impl.get_log(log_type=log_type)
	
	@requires_driver
	def _log_types_impl(self) -> Any:
		return self._driver_impl.log_types
