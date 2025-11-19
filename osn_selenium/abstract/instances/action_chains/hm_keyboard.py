from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT


__all__ = ["AbstractHMKeyboardMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractHMKeyboardMixin(ABC):
	"""
	Mixin class providing abstract methods for human-like keyboard interactions.
	"""
	
	@abstractmethod
	def hm_send_keys(self, text: str) -> "AbstractActionChains":
		"""
		Simulates human-like text input with variable delays.

		Args:
			text (str): The text to be typed.

		Returns:
			"AbstractActionChains": The instance for method chaining.
		"""
		
		...
	
	@abstractmethod
	def hm_send_keys_to_element(self, element: WEB_ELEMENT_TYPEHINT, text: str) -> "AbstractActionChains":
		"""
		Simulates human-like text input into a specific element with variable delays.

		Args:
			element (WEB_ELEMENT_TYPEHINT): The target element to type into.
			text (str): The text to be typed.

		Returns:
			"AbstractActionChains": The instance for method chaining.
		"""
		
		...
