from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT


__all__ = ["AbstractDragAndDropMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractDragAndDropMixin(ABC):
	"""
	Mixin class providing abstract methods for drag and drop interactions.
	"""
	
	@abstractmethod
	def drag_and_drop(self, source: WEB_ELEMENT_TYPEHINT, target: WEB_ELEMENT_TYPEHINT) -> "AbstractActionChains":
		"""
		Drags an element and drops it onto another element.

		Args:
			source (WEB_ELEMENT_TYPEHINT): The element to drag.
			target (WEB_ELEMENT_TYPEHINT): The element to drop on.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def drag_and_drop_by_offset(self, source: WEB_ELEMENT_TYPEHINT, xoffset: int, yoffset: int) -> "AbstractActionChains":
		"""
		Drags an element by a given offset.

		Args:
			source (WEB_ELEMENT_TYPEHINT): The element to drag.
			xoffset (int): The horizontal offset to drag by.
			yoffset (int): The vertical offset to drag by.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
