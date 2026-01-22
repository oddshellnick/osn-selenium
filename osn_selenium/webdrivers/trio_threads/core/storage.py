from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.instances.trio_threads.storage import Storage
from osn_selenium.webdrivers.trio_threads.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.storage import (
	AbstractCoreStorageMixin
)


class CoreStorageMixin(CoreBaseMixin, AbstractCoreStorageMixin):
	"""
	Mixin for managing browser storage and cookies in Core WebDrivers.

	Provides methods to add, retrieve, and delete cookies, as well as access
	other storage mechanisms.
	"""
	
	@requires_driver
	async def add_cookie(self, cookie_dict: Dict[str, Any]) -> None:
		await self.sync_to_trio(sync_function=self.driver.add_cookie)(cookie_dict=cookie_dict)
	
	@requires_driver
	async def delete_all_cookies(self) -> None:
		await self.sync_to_trio(sync_function=self.driver.delete_all_cookies)()
	
	@requires_driver
	async def delete_cookie(self, name: str) -> None:
		await self.sync_to_trio(sync_function=self.driver.delete_cookie)(name=name)
	
	@requires_driver
	async def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self.driver.get_cookie)(name=name)
	
	@requires_driver
	async def get_cookies(self) -> List[Dict[str, Any]]:
		return await self.sync_to_trio(sync_function=self.driver.get_cookies)()
	
	@requires_driver
	async def storage(self) -> Storage:
		legacy = await self.sync_to_trio(sync_function=lambda: self.driver.storage)()
		
		return Storage(
				selenium_storage=legacy,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
