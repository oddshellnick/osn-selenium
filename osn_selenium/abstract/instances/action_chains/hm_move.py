from abc import ABC, abstractmethod
from osn_selenium.models import Point
from typing import TYPE_CHECKING, Tuple
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT


__all__ = ["AbstractHMMoveMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractHMMoveMixin(ABC):
	"""
	Mixin class providing abstract methods for human-like mouse movement interactions.
	"""
	
	@abstractmethod
	def hm_move(self, start_position: Point, end_position: Point) -> "AbstractActionChains":
		"""
		Moves the mouse cursor from a start to an end position in a human-like curve.

		Args:
			start_position (Point): The starting coordinates.
			end_position (Point): The ending coordinates.

		Returns:
			AbstractActionChains: The instance for method chaining.
		"""
		
		...
	
	@abstractmethod
	def hm_move_by_offset(self, start_position: Point, xoffset: int, yoffset: int) -> Tuple["AbstractActionChains", Point]:
		"""
		Moves the mouse cursor by a given offset from a starting Point in a human-like way.

		Args:
			start_position (Point): The starting coordinates of the mouse.
			xoffset (int): The horizontal offset to move by.
			yoffset (int): The vertical offset to move by.

		Returns:
			Tuple[AbstractActionChains, Point]: A tuple containing the instance for
				method chaining and the final Point coordinates of the cursor.
		"""
		
		...
	
	@abstractmethod
	def hm_move_to_element(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple["AbstractActionChains", Point]:
		"""
		Moves the mouse cursor to the center of an element in a human-like way.

		Args:
			start_position (Point): The starting coordinates of the mouse.
			element (WEB_ELEMENT_TYPEHINT): The target element to move to.

		Returns:
			Tuple[AbstractActionChains, Point]: A tuple containing the instance for
				method chaining and the final Point coordinates of the cursor.
		"""
		
		...
	
	@abstractmethod
	def hm_move_to_element_with_offset(
			self,
			start_position: Point,
			element: WEB_ELEMENT_TYPEHINT,
			xoffset: int,
			yoffset: int
	) -> Tuple["AbstractActionChains", Point]:
		"""
		Moves the mouse cursor to a specific offset within an element in a human-like way.

		Args:
			start_position (Point): The starting coordinates of the mouse.
			element (WEB_ELEMENT_TYPEHINT): The target element.
			xoffset (int): The horizontal offset from the element's top-left corner.
			yoffset (int): The vertical offset from the element's top-left corner.

		Returns:
			Tuple[AbstractActionChains, Point]: A tuple containing the instance for
				method chaining and the final Point coordinates of the cursor.
		"""
		
		...
	
	@abstractmethod
	def hm_move_to_element_with_random_offset(self, start_position: Point, element: WEB_ELEMENT_TYPEHINT) -> Tuple["AbstractActionChains", Point]:
		"""
		Moves the mouse cursor to a random Point within an element in a human-like way.

		Args:
			start_position (Point): The starting coordinates of the mouse.
			element (WEB_ELEMENT_TYPEHINT): The target element to move to.

		Returns:
			Tuple[AbstractActionChains, Point]: A tuple containing the instance for
				method chaining and the final Point coordinates of the cursor.
		"""
		
		...
