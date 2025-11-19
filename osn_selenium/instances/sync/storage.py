from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.abstract.instances.storage import AbstractStorage
from selenium.webdriver.common.bidi.storage import (
	BrowsingContextPartitionDescriptor,
	CookieFilter,
	DeleteCookiesResult,
	GetCookiesResult,
	PartialCookie,
	SetCookieResult,
	Storage as legacyStorage,
	StorageKeyPartitionDescriptor
)


class Storage(AbstractStorage):
	def __init__(self, selenium_storage: legacyStorage,) -> None:
		self._selenium_storage = selenium_storage
	
	def delete_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> DeleteCookiesResult:
		return self.legacy.delete_cookies(filter=filter, partition=partition)
	
	@classmethod
	def from_legacy(cls, selenium_storage: legacyStorage,) -> Self:
		"""
		Creates an instance from a legacy Selenium Storage object.

		This factory method is used to wrap an existing Selenium Storage
		instance into the new interface.

		Args:
			selenium_storage (legacyStorage): The legacy Selenium Storage instance.

		Returns:
			Self: A new instance of a class implementing Storage.
		"""
		
		return cls(selenium_storage=selenium_storage)
	
	def get_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> GetCookiesResult:
		return self.legacy.get_cookies(filter=filter, partition=partition)
	
	@property
	def legacy(self) -> legacyStorage:
		return self._selenium_storage
	
	def set_cookie(
			self,
			cookie: PartialCookie,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> SetCookieResult:
		return self.legacy.set_cookie(cookie=cookie, partition=partition)
