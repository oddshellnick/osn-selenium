from abc import ABC, abstractmethod


__all__ = ["AbstractCoreNavigationMixin"]


class AbstractCoreNavigationMixin(ABC):
	"""Mixin responsible for page navigation."""
	
	@abstractmethod
	def back(self) -> None:
		"""
		Goes one step backward in the browser history.
		"""
		
		...
	
	@abstractmethod
	def current_url(self) -> str:
		"""
		Gets the URL of the current page.

		Returns:
			str: The URL of the current page.
		"""
		
		...
	
	@abstractmethod
	def forward(self) -> None:
		"""
		Goes one step forward in the browser history.
		"""
		
		...
	
	@abstractmethod
	def get(self, url: str) -> None:
		"""
		Loads a web page in the current browser session.

		Args:
			url (str): The URL to load.
		"""
		
		...
	
	@abstractmethod
	def refresh(self) -> None:
		"""
		Refreshes the current page.
		"""
		
		...
	
	@abstractmethod
	def title(self) -> str:
		"""
		Gets the title of the current page.

		Returns:
			str: The title of the current page.
		"""
		
		...
