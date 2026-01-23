from typing import Any, Dict
from osn_selenium.webdrivers.unified.blink.features import (
	UnifiedBlinkFeaturesMixin
)
from osn_selenium.abstract.webdriver.blink.features import (
	AbstractBlinkFeaturesMixin
)


__all__ = ["BlinkFeaturesMixin"]


class BlinkFeaturesMixin(UnifiedBlinkFeaturesMixin, AbstractBlinkFeaturesMixin):
	"""
	Mixin for managing browser features and capabilities for Blink WebDrivers.

	Provides interfaces to query, enable, or disable specific browser features
	and inspect the supported capabilities of the current session.
	"""
	
	def get_issue_message(self) -> Any:
		return self._get_issue_message_impl()
	
	def launch_app(self, id: str) -> Dict[str, Any]:
		return self._launch_app_impl(id=id)
	
	def set_permissions(self, name: str, value: str) -> None:
		self._set_permissions_impl(name=name, value=value)
