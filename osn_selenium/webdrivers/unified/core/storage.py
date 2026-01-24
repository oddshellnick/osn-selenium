from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.webdrivers._decorators import requires_driver
from osn_selenium.webdrivers.unified.core.base import UnifiedCoreBaseMixin


__all__ = ["UnifiedCoreStorageMixin"]


class UnifiedCoreStorageMixin(UnifiedCoreBaseMixin):
	@requires_driver
	def _add_cookie_impl(self, cookie_dict: Dict[str, Any]) -> None:
		self._driver_impl.add_cookie(cookie_dict=cookie_dict)
	
	@requires_driver
	def _delete_all_cookies_impl(self) -> None:
		self._driver_impl.delete_all_cookies()
	
	@requires_driver
	def _delete_cookie_impl(self, name: str) -> None:
		self._driver_impl.delete_cookie(name=name)
	
	@requires_driver
	def _get_cookie_impl(self, name: str) -> Optional[Dict[str, Any]]:
		return self._driver_impl.get_cookie(name=name)
	
	@requires_driver
	def _get_cookies_impl(self) -> List[Dict[str, Any]]:
		return self._driver_impl.get_cookies()
	
	@requires_driver
	def _storage_impl(self) -> Any:
		return self._driver_impl.storage
