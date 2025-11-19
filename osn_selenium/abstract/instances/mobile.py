from typing import Any, Sequence
from abc import ABC, abstractmethod
from selenium.webdriver.remote.mobile import (
	Mobile as legacyMobile
)


__all__ = ["AbstractMobile"]


class AbstractMobile(ABC):
	"""
	Abstract base class for mobile-specific interactions.

	Defines the interface for managing network connections and contexts
	in a mobile environment.
	"""
	
	@abstractmethod
	def context(self) -> str:
		"""
		The current context handle.
		"""
		
		...
	
	@abstractmethod
	def contexts(self) -> Sequence[str]:
		"""
		A sequence of available context handles.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyMobile:
		"""
		Returns the underlying legacy Selenium Mobile instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyMobile: The legacy Selenium Mobile object.
		"""
		
		...
	
	@property
	@abstractmethod
	def network_connection(self) -> Any:
		"""
		The current network connection type.
		"""
		
		...
	
	@abstractmethod
	def set_context(self, new_context: str) -> None:
		"""
		Sets the current context.

		Args:
			new_context (str): The handle of the context to switch to.
		"""
		
		...
	
	@abstractmethod
	def set_network_connection(self, network: Any) -> None:
		"""
		Sets the network connection type.

		Args:
			network (Any): The network type to set.
		"""
		
		...
