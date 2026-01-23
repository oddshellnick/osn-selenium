from abc import ABC, abstractmethod
from typing import (
	Optional,
	TYPE_CHECKING
)
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


__all__ = ["AbstractHMScrollMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractHMScrollMixin(ABC):
	"""
	Mixin class providing abstract methods for human-like scrolling interactions.
	"""
	
	@abstractmethod
	def hm_scroll_by_amount(self, delta_x: int, delta_y: int) -> "AbstractActionChains":
		"""
		Simulates smooth, human-like scrolling by a specific amount.

		Args:
			delta_x (int): The horizontal distance to scroll.
			delta_y (int): The vertical distance to scroll.

		Returns:
			AbstractActionChains: The instance for method chaining.
		"""
		
		...
	
	@abstractmethod
	def hm_scroll_from_origin(self, delta_x: int, delta_y: int, origin: Optional[ScrollOrigin] = None) -> "AbstractActionChains":
		"""
		Simulates smooth, human-like scrolling from a specific origin.

		Args:
			delta_x (int): The horizontal distance to scroll.
			delta_y (int): The vertical distance to scroll.
			origin (Optional[ScrollOrigin]): The origin Point for scrolling. If None, it's determined automatically.

		Returns:
			AbstractActionChains: The instance for method chaining.
		"""
		
		...
	
	@abstractmethod
	def hm_scroll_to_element(
			self,
			element: WEB_ELEMENT_TYPEHINT,
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0
	) -> "AbstractActionChains":
		"""
		Scrolls smoothly to bring an element into view, avoiding viewport edges.

		Args:
			element (WEB_ELEMENT_TYPEHINT): The target element to scroll to.
			additional_lower_y_offset (int): Additional offset from the bottom edge of the viewport.
			additional_upper_y_offset (int): Additional offset from the top edge of the viewport.
			additional_right_x_offset (int): Additional offset from the right edge of the viewport.
			additional_left_x_offset (int): Additional offset from the left edge of the viewport.

		Returns:
			AbstractActionChains: The instance for method chaining.
		"""
		
		...
