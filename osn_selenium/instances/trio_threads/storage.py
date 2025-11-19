import trio
from typing import (
	Optional,
	Self,
	Union
)
from osn_selenium.abstract.instances.storage import AbstractStorage
from osn_selenium.instances.trio_threads.base_mixin import _TrioThreadMixin
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


class Storage(_TrioThreadMixin, AbstractStorage):
	def __init__(
			self,
			selenium_storage: legacyStorage,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> None:
		super().__init__(lock=lock, limiter=limiter)
		
		self._selenium_storage = selenium_storage
	
	async def delete_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> DeleteCookiesResult:
		return await self._wrap_to_trio(self.legacy.delete_cookies, filter=filter, partition=partition)
	
	@classmethod
	def from_legacy(
			cls,
			selenium_storage: legacyStorage,
			lock: trio.Lock,
			limiter: trio.CapacityLimiter,
	) -> Self:
		"""
		Creates an instance from a legacy Selenium Storage object.

		This factory method is used to wrap an existing Selenium Storage
		instance into the new interface.

		Args:
			selenium_storage (legacyStorage): The legacy Selenium Storage instance.
			lock (trio.Lock): A Trio lock for managing concurrent access.
			limiter (trio.CapacityLimiter): A Trio capacity limiter for rate limiting.

		Returns:
			Self: A new instance of a class implementing Storage.
		"""
		
		return cls(selenium_storage=selenium_storage, lock=lock, limiter=limiter)
	
	async def get_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> GetCookiesResult:
		return await self._wrap_to_trio(self.legacy.get_cookies, filter=filter, partition=partition)
	
	@property
	def legacy(self) -> legacyStorage:
		return self._selenium_storage
	
	async def set_cookie(
			self,
			cookie: PartialCookie,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> SetCookieResult:
		return await self._wrap_to_trio(self.legacy.set_cookie, cookie=cookie, partition=partition)
