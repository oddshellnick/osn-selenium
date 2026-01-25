from abc import ABC, abstractmethod
from typing import (
	Any,
	Callable,
	Optional,
	Sequence
)
from selenium.webdriver.common.bidi.network import (
	Network as legacyNetwork
)


__all__ = ["AbstractNetwork"]


class AbstractNetwork(ABC):
	"""
	Abstract base class for network interception.

	Defines the interface for adding and removing handlers for network events
	and authentication challenges.
	"""
	
	@abstractmethod
	def add_auth_handler(self, username: str, password: str) -> None:
		"""
		Adds a handler for authentication challenges.

		Args:
			username (str): The username for authentication.
			password (str): The password for authentication.
		"""
		
		...
	
	@abstractmethod
	def add_request_handler(
			self,
			event: Any,
			callback: Callable,
			url_patterns: Optional[Sequence[str]] = None,
			contexts: Optional[Sequence[str]] = None,
	) -> None:
		"""
		Adds a handler for a network request event.

		Args:
			event (Any): The network event to listen for.
			callback (Callable): The function to call when the event occurs.
			url_patterns (Optional[Sequence[str]]): URL patterns to filter requests.
			contexts (Optional[Sequence[str]]): Browsing context IDs to filter requests.
		"""
		
		...
	
	@abstractmethod
	def clear_request_handlers(self) -> None:
		"""
		Clears all registered network request handlers.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyNetwork:
		"""
		Returns the underlying legacy Selenium Network instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyNetwork: The legacy Selenium Network object.
		"""
		
		...
	
	@abstractmethod
	def remove_auth_handler(self, callback_id: str) -> None:
		"""
		Removes an authentication handler.

		Args:
			callback_id (str): The ID of the handler to remove.
		"""
		
		...
	
	@abstractmethod
	def remove_request_handler(self, event: Any, callback_id: str) -> None:
		"""
		Removes a network request handler.

		Args:
			event (Any): The network event to stop listening to.
			callback_id (str): The ID of the handler to remove.
		"""
		
		...
