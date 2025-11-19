from typing import Optional, Union
from abc import ABC, abstractmethod
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


__all__ = ["AbstractStorage"]


class AbstractStorage(ABC):
	"""
	Abstract base class for interacting with browser storage.

	Defines the interface for managing cookies within different browsing contexts.
	"""
	
	@abstractmethod
	def delete_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> DeleteCookiesResult:
		"""
		Deletes cookies.

		Args:
			filter (Optional[CookieFilter]): A filter to select which cookies to delete.
			partition (Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]]):
				The storage partition to delete cookies from.

		Returns:
			DeleteCookiesResult: The result of the delete cookies operation.
		"""
		
		...
	
	@abstractmethod
	def get_cookies(
			self,
			filter: Optional[CookieFilter] = None,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> GetCookiesResult:
		"""
		Gets cookies from the browser.

		Args:
			filter (Optional[CookieFilter]): A filter to apply to the cookies.
			partition (Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]]):
				The storage partition to retrieve cookies from.

		Returns:
			GetCookiesResult: The result containing the retrieved cookies.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyStorage:
		"""
		Returns the underlying legacy Selenium Storage instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyStorage: The legacy Selenium Storage object.
		"""
		
		...
	
	@abstractmethod
	def set_cookie(
			self,
			cookie: PartialCookie,
			partition: Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]] = None,
	) -> SetCookieResult:
		"""
		Sets a cookie.

		Args:
			cookie (PartialCookie): The cookie to set.
			partition (Optional[Union[BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor]]):
				The storage partition to set the cookie in.

		Returns:
			SetCookieResult: The result of the set cookie operation.
		"""
		
		...
