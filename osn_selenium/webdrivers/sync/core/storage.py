from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.instances.sync.storage import Storage
from osn_selenium.instances.convert import (
	get_sync_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.storage import (
	UnifiedCoreStorageMixin
)
from osn_selenium.abstract.webdriver.core.storage import (
	AbstractCoreStorageMixin
)


__all__ = ["CoreStorageMixin"]


class CoreStorageMixin(UnifiedCoreStorageMixin, AbstractCoreStorageMixin):
	"""
	Mixin for managing browser storage and cookies in Core WebDrivers.

	Provides methods to add, retrieve, and delete cookies, as well as access
	other storage mechanisms.
	"""
	
	def add_cookie(self, cookie_dict: Dict[str, Any]) -> None:
		self._add_cookie_impl(cookie_dict=cookie_dict)
	
	def delete_all_cookies(self) -> None:
		self._delete_all_cookies_impl()
	
	def delete_cookie(self, name: str) -> None:
		self._delete_cookie_impl(name=name)
	
	def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		return self._get_cookie_impl(name=name)
	
	def get_cookies(self) -> List[Dict[str, Any]]:
		return self._get_cookies_impl()
	
	def storage(self) -> Storage:
		legacy = self._storage_impl()
		
		return get_sync_instance_wrapper(wrapper_class=Storage, legacy_object=legacy)
