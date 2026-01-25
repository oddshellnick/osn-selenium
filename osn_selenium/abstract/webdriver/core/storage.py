from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.instances.storage import AbstractStorage


__all__ = ["AbstractCoreStorageMixin"]


class AbstractCoreStorageMixin(ABC):
	"""Mixin responsible for cookies and storage."""
	
	@abstractmethod
	def add_cookie(self, cookie_dict: Dict[str, Any]) -> None:
		"""
		Adds a cookie to the current session.

		Args:
			cookie_dict (Dict[str, Any]): A dictionary representing the cookie to add.
		"""
		
		...
	
	@abstractmethod
	def delete_all_cookies(self) -> None:
		"""
		Deletes all cookies for the current session.
		"""
		
		...
	
	@abstractmethod
	def delete_cookie(self, name: str) -> None:
		"""
		Deletes a single cookie with the given name.

		Args:
			name (str): The name of the cookie to delete.
		"""
		
		...
	
	@abstractmethod
	def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
		"""
		Gets a single cookie with the given name.

		Args:
			name (str): The name of the cookie.

		Returns:
			Optional[Dict[str, Any]]: The cookie dictionary, or None if not found.
		"""
		
		...
	
	@abstractmethod
	def get_cookies(self) -> List[Dict[str, Any]]:
		"""
		Returns all cookies for the current session.

		Returns:
			List[Dict[str, Any]]: A list of dictionaries, each representing a cookie.
		"""
		
		...
	
	@abstractmethod
	def storage(self) -> AbstractStorage:
		"""
		Provides access to the browser's storage mechanisms (e.g., cookies, local storage).

		Returns:
			AbstractStorage: An object for interacting with browser storage.
		"""
		
		...
