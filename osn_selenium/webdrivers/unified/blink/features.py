from typing import Any, Dict
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.blink.base import (
	UnifiedBlinkBaseMixin
)


__all__ = ["UnifiedBlinkFeaturesMixin"]


class UnifiedBlinkFeaturesMixin(UnifiedBlinkBaseMixin):
	@requires_driver
	def _get_issue_message_impl(self) -> Any:
		return self._driver_impl.get_issue_message()
	
	@requires_driver
	def _launch_app_impl(self, id: str) -> Dict[str, Any]:
		return self._driver_impl.launch_app(id=id)
	
	@requires_driver
	def _set_permissions_impl(self, name: str, value: str) -> None:
		self._driver_impl.set_permissions(name=name, value=value)
