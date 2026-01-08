from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.instances.sync.storage import Storage
from osn_selenium.webdrivers.decorators import requires_driver
from osn_selenium.webdrivers.sync.core.base import CoreBaseMixin
from osn_selenium.abstract.webdriver.core.storage import (
	AbstractCoreStorageMixin
)


class CoreStorageMixin(CoreBaseMixin, AbstractCoreStorageMixin):
	@requires_driver
	def add_cookie(self, cookie_dict: Dict[str, Any]) -> None:
		self.driver.add_cookie(cookie_dict=cookie_dict)
	
	@requires_driver
	def delete_all_cookies(self) -> None:
		self.driver.delete_all_cookies()
	
	@requires_driver
	def delete_cookie(self, name: str) -> None:
		self.driver.delete_cookie(name=name)
	
	@requires_driver
	def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		return self.driver.get_cookie(name=name)
	
	@requires_driver
	def get_cookies(self) -> List[Dict[str, Any]]:
		return self.driver.get_cookies()
	
	@requires_driver
	def storage(self) -> Storage:
		legacy = self.driver.storage
		
		return Storage(selenium_storage=legacy)
