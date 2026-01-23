from typing import Optional, Union
from osn_selenium.exceptions.instance import NotExpectedTypeError
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


__all__ = ["UnifiedStorage"]


class UnifiedStorage:
	def __init__(self, selenium_storage: legacyStorage):
		if not isinstance(selenium_storage, legacyStorage):
			raise NotExpectedTypeError(expected_type=legacyStorage, received_instance=selenium_storage)
		
		self._selenium_storage = selenium_storage
	
	def _delete_cookies_impl(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> DeleteCookiesResult:
		return self._legacy_impl.delete_cookies(filter=filter, partition=partition)
	
	def _get_cookies_impl(
			self,
			filter: Optional[CookieFilter],
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> GetCookiesResult:
		return self._legacy_impl.get_cookies(filter=filter, partition=partition)
	
	@property
	def _legacy_impl(self) -> legacyStorage:
		return self._selenium_storage
	
	def _set_cookie_impl(
			self,
			cookie: PartialCookie,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> SetCookieResult:
		return self._legacy_impl.set_cookie(cookie=cookie, partition=partition)
