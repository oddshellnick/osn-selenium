from abc import ABC, abstractmethod
from typing import (
	Optional,
	TYPE_CHECKING
)
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT


__all__ = ["AbstractClickMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractClickMixin(ABC):
	"""
	Mixin class providing abstract methods for mouse click interactions.
	"""
	
	@abstractmethod
	def click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "AbstractActionChains":
		"""
		Performs a click action.

		Args:
			on_element (Optional[WEB_ELEMENT_TYPEHINT]): The element to click.
				If None, clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def click_and_hold(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "AbstractActionChains":
		"""
		Clicks and holds the mouse button down.

		Args:
			on_element (Optional[WEB_ELEMENT_TYPEHINT]): The element to click on.
				If None, clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def context_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "AbstractActionChains":
		"""
		Performs a right-click action.

		Args:
			on_element (Optional[WEB_ELEMENT_TYPEHINT]): The element to right-click.
				If None, right-clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def double_click(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "AbstractActionChains":
		"""
		Performs a double-click action.

		Args:
			on_element (Optional[WEB_ELEMENT_TYPEHINT]): The element to double-click.
				If None, double-clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def release(self, on_element: Optional[WEB_ELEMENT_TYPEHINT]) -> "AbstractActionChains":
		"""
		Releases a held mouse button.

		Args:
			on_element (Optional[WEB_ELEMENT_TYPEHINT]): The element on which to release the button.
				If None, releases at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
