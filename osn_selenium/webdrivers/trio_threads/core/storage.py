from osn_selenium.trio_threads_mixin import TrioThreadMixin
from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.instances.trio_threads.storage import Storage
from osn_selenium.instances.convert import (
	get_trio_thread_instance_wrapper
)
from osn_selenium.webdrivers.unified.core.storage import (
	UnifiedCoreStorageMixin
)
from osn_selenium.abstract.webdriver.core.storage import (
	AbstractCoreStorageMixin
)


__all__ = ["CoreStorageMixin"]


class CoreStorageMixin(UnifiedCoreStorageMixin, TrioThreadMixin, AbstractCoreStorageMixin):
	"""
	Mixin for managing browser storage and cookies in Core WebDrivers.

	Provides methods to add, retrieve, and delete cookies, as well as access
	other storage mechanisms.
	"""
	
	async def add_cookie(self, cookie_dict: Dict[str, Any]) -> None:
		await self.sync_to_trio(sync_function=self._add_cookie_impl)(cookie_dict=cookie_dict)
	
	async def delete_all_cookies(self) -> None:
		await self.sync_to_trio(sync_function=self._delete_all_cookies_impl)()
	
	async def delete_cookie(self, name: str) -> None:
		await self.sync_to_trio(sync_function=self._delete_cookie_impl)(name=name)
	
	async def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_cookie_impl)(name=name)
	
	async def get_cookies(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self._get_cookies_impl)()
	
	async def storage(self) -> Storage:
		legacy = await self.sync_to_trio(sync_function=self._storage_impl)()
		
		return get_trio_thread_instance_wrapper(
				wrapper_class=Storage,
				legacy_object=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
