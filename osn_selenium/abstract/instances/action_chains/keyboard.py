from abc import ABC, abstractmethod
from typing import (
	Optional,
	TYPE_CHECKING
)
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT


__all__ = ["AbstractKeyboardMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractKeyboardMixin(ABC):
	"""
	Mixin class providing abstract methods for keyboard interactions.
	"""
	
	@abstractmethod
	def key_down(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT]) -> "AbstractActionChains":
		"""
		Performs a key press without releasing it.

		Args:
			value (str): The key to press (e.g., Keys.CONTROL).
			element (Optional[WEB_ELEMENT_TYPEHINT]): The element to focus before pressing the key.
				If None, the key is pressed without focusing on an element.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def key_up(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT]) -> "AbstractActionChains":
		"""
		Performs a key release.

		Args:
			value (str): The key to release (e.g., Keys.CONTROL).
			element (Optional[WEB_ELEMENT_TYPEHINT]): The element to focus before releasing the key.
				If None, the key is released without focusing on an element.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def send_keys(self, *keys_to_send: str) -> "AbstractActionChains":
		"""
		Sends keys to the current focused element.

		Args:
			keys_to_send (str): The keys to send.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def send_keys_to_element(self, element: WEB_ELEMENT_TYPEHINT, *keys_to_send: str) -> "AbstractActionChains":
		"""
		Sends keys to a specific element.

		Args:
			element (WEB_ELEMENT_TYPEHINT): The element to send keys to.
			keys_to_send (str): The keys to send.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
