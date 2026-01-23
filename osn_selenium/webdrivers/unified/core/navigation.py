from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin


__all__ = ["UnifiedCoreNavigationMixin"]


class UnifiedCoreNavigationMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _back_impl(self) -> None:
		self._driver_impl.back()
	
	@requires_driver
	def _current_url_impl(self) -> str:
		return self._driver_impl.current_url
	
	@requires_driver
	def _forward_impl(self) -> None:
		self._driver_impl.forward()
	
	@requires_driver
	def _get_impl(self, url: str) -> None:
		self._driver_impl.get(url=url)
	
	@requires_driver
	def _refresh_impl(self) -> None:
		self._driver_impl.refresh()
	
	@requires_driver
	def _title_impl(self) -> str:
		return self._driver_impl.title
