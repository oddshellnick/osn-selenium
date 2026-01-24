from typing import Any
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin


__all__ = ["UnifiedCoreComponentsMixin"]


class UnifiedCoreComponentsMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _browser_impl(self) -> Any:
		return self._driver_impl.browser
	
	@requires_driver
	def _browsing_context_impl(self) -> Any:
		return self._driver_impl.browsing_context
	
	@requires_driver
	def _dialog_impl(self) -> Any:
		return self._driver_impl.dialog
	
	@requires_driver
	def _mobile_impl(self) -> Any:
		return self._driver_impl.mobile
	
	@requires_driver
	def _permissions_impl(self) -> Any:
		return self._driver_impl.permissions
	
	@requires_driver
	def _webextension_impl(self) -> Any:
		return self._driver_impl.webextension
