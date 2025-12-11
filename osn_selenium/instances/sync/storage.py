from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.instances.types import STORAGE_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
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
	def __init__(self, selenium_storage: legacyStorage) -> None:
		if not isinstance(selenium_storage, legacyStorage):
			raise TypeError(f"Expected {type(legacyStorage)}, got {type(selenium_storage)}")
		
		self._selenium_storage = selenium_storage
	
	def delete_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> DeleteCookiesResult:
		return self.legacy.delete_cookies(filter=filter, partition=partition)
	
	@classmethod
	def from_legacy(cls, selenium_storage: STORAGE_TYPEHINT) -> Self:
		legacy_storage_obj = get_legacy_instance(selenium_storage)
		
		if not isinstance(legacy_storage_obj, legacyStorage):
			raise TypeError(
					f"Could not convert input to {type(legacyStorage)}: {type(selenium_storage)}"
			)
		
		return cls(selenium_storage=legacy_storage_obj)
	
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
