from typing import Sequence
from abc import ABC, abstractmethod
from selenium.webdriver.common.bidi.browser import (
	Browser as legacyBrowser,
	ClientWindowInfo
)


__all__ = ["AbstractBrowser"]


class AbstractBrowser(ABC):
	"""
	Abstract base class for browser-level interactions.

	Defines the interface for managing user contexts and client windows.
	"""
	
	@abstractmethod
	def create_user_context(self) -> str:
		"""
		Creates a new user context.

		Returns:
			str: The ID of the newly created user context.
		"""
		
		...
	
	@abstractmethod
	def get_client_windows(self) -> Sequence[ClientWindowInfo]:
		"""
		Gets information about all client windows.

		Returns:
			Sequence[ClientWindowInfo]: A sequence of ClientWindowInfo objects.
		"""
		
		...
	
	@abstractmethod
	def get_user_contexts(self) -> Sequence[str]:
		"""
		Gets a list of all user context IDs.

		Returns:
			Sequence[str]: A sequence of user context IDs.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyBrowser:
		"""
		Returns the underlying legacy Selenium Browser instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyBrowser: The legacy Selenium Browser object.
		"""
		
		...
	
	@abstractmethod
	def remove_user_context(self, user_context_id: str) -> None:
		"""
		Removes a user context.

		Args:
			user_context_id (str): The ID of the user context to remove.
		"""
		
		...
