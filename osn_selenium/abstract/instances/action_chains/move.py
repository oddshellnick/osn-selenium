from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT


__all__ = ["AbstractMoveMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractMoveMixin(ABC):
	"""
	Mixin class providing abstract methods for mouse movement interactions.
	"""
	
	@abstractmethod
	def move_by_offset(self, xoffset: int, yoffset: int) -> "AbstractActionChains":
		"""
		Moves the mouse to an offset from the current position.

		Args:
			xoffset (int): The horizontal offset to move by.
			yoffset (int): The vertical offset to move by.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def move_to_element(self, to_element: WEB_ELEMENT_TYPEHINT) -> "AbstractActionChains":
		"""
		Moves the mouse to the middle of the specified element.

		Args:
			to_element (WEB_ELEMENT_TYPEHINT): The element to move to.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def move_to_element_with_offset(self, to_element: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> "AbstractActionChains":
		"""
		Moves the mouse to an offset from the center of an element.

		Args:
			to_element (WEB_ELEMENT_TYPEHINT): The element to move to.
			xoffset (int): The horizontal offset from the element's center.
			yoffset (int): The vertical offset from the element's center.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
