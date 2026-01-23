from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.instances._typehints import STORAGE_TYPEHINT
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances.unified.storage import UnifiedStorage
from osn_selenium.abstract.instances.storage import AbstractStorage
from osn_selenium.exceptions.instance import (
	CannotConvertTypeError
)
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


__all__ = ["Storage"]


class Storage(UnifiedStorage, AbstractStorage):
	"""
	Wrapper for the legacy Selenium BiDi Storage instance.

	Manages browser storage mechanisms, primarily focusing on getting, setting,
	and deleting cookies with specific filters and partition descriptors.
	"""
	
	def __init__(self, selenium_storage: legacyStorage) -> None:
		"""
		Initializes the Storage wrapper.

		Args:
			selenium_storage (legacyStorage): The legacy Selenium Storage instance to wrap.
		"""
		
		UnifiedStorage.__init__(self, selenium_storage=selenium_storage)
	
	def delete_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> DeleteCookiesResult:
		return self._delete_cookies_impl(filter=filter, partition=partition)
	
	@classmethod
	def from_legacy(cls, legacy_object: STORAGE_TYPEHINT) -> Self:
		"""
		Creates an instance from a legacy Selenium Storage object.

		This factory method is used to wrap an existing Selenium Storage
		instance into the new interface.

		Args:
			legacy_object (STORAGE_TYPEHINT): The legacy Selenium Storage instance or its wrapper.

		Returns:
			Self: A new instance of a class implementing Storage.
		"""
		
		legacy_storage_obj = get_legacy_instance(instance=legacy_object)
		
		if not isinstance(legacy_storage_obj, legacyStorage):
			raise CannotConvertTypeError(from_=legacyStorage, to_=legacy_object)
		
		return cls(selenium_storage=legacy_storage_obj)
	
	def get_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> GetCookiesResult:
		return self._get_cookies_impl(filter=filter, partition=partition)
	
	@property
	def legacy(self) -> legacyStorage:
		return self._legacy_impl
	
	def set_cookie(
			self,
			cookie: PartialCookie,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> SetCookieResult:
		return self._set_cookie_impl(cookie=cookie, partition=partition)
