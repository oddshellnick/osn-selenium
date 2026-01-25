from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


__all__ = ["AbstractScrollMixin"]

if TYPE_CHECKING:
	from osn_selenium.abstract.instances.action_chains import AbstractActionChains


class AbstractScrollMixin(ABC):
	"""
	Mixin class providing abstract methods for wheel/scroll interactions.
	"""
	
	@abstractmethod
	def scroll_by_amount(self, delta_x: int, delta_y: int) -> "AbstractActionChains":
		"""
		Scrolls by a given amount from the current position.

		Args:
			delta_x (int): The horizontal scroll amount.
			delta_y (int): The vertical scroll amount.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def scroll_from_origin(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int) -> "AbstractActionChains":
		"""
		Scrolls from a specific origin Point by a given offset.

		Args:
			scroll_origin (ScrollOrigin): The origin Point to start scrolling from.
			delta_x (int): The horizontal scroll amount.
			delta_y (int): The vertical scroll amount.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def scroll_to_element(self, element: WEB_ELEMENT_TYPEHINT) -> "AbstractActionChains":
		"""
		Scrolls the view to bring the element into view.

		Args:
			element (WEB_ELEMENT_TYPEHINT): The element to scroll to.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
