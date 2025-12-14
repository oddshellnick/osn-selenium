from abc import ABC, abstractmethod
from typing import (
	Optional,
	Self,
	Tuple,
	TYPE_CHECKING, Union
)
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


if TYPE_CHECKING:
	from osn_selenium.instances.types import Point, WEB_ELEMENT_TYPEHINT

class AbstractActionChains(ABC):
	"""
	Abstract base class for action chains.

	Defines the interface for building a sequence of user actions like
	mouse movements, button clicks, and keyboard events.
	"""
	
	@abstractmethod
	def click(self, on_element: Optional["WEB_ELEMENT_TYPEHINT"] = None,) -> Self:
		"""
		Performs a click action.

		Args:
			on_element (Optional["WEB_ELEMENT_TYPEHINT"]): The element to click.
				If None, clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def click_and_hold(self, on_element: Optional["WEB_ELEMENT_TYPEHINT"] = None,) -> Self:
		"""
		Clicks and holds the mouse button down.

		Args:
			on_element (Optional["WEB_ELEMENT_TYPEHINT"]): The element to click on.
				If None, clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def context_click(self, on_element: Optional["WEB_ELEMENT_TYPEHINT"] = None,) -> Self:
		"""
		Performs a right-click action.

		Args:
			on_element (Optional["WEB_ELEMENT_TYPEHINT"]): The element to right-click.
				If None, right-clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def double_click(self, on_element: Optional["WEB_ELEMENT_TYPEHINT"] = None,) -> Self:
		"""
		Performs a double-click action.

		Args:
			on_element (Optional["WEB_ELEMENT_TYPEHINT"]): The element to double-click.
				If None, double-clicks at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def drag_and_drop(
			self,
			source_element: "WEB_ELEMENT_TYPEHINT",
			target_element: "WEB_ELEMENT_TYPEHINT",
	) -> Self:
		"""
		Drags an element and drops it onto another element.

		Args:
			source_element ("WEB_ELEMENT_TYPEHINT"): The element to drag.
			target_element ("WEB_ELEMENT_TYPEHINT"): The element to drop on.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def drag_and_drop_by_offset(
			self,
			source_element: "WEB_ELEMENT_TYPEHINT",
			xoffset: int,
			yoffset: int,
	) -> Self:
		"""
		Drags an element by a given offset.

		Args:
			source_element ("WEB_ELEMENT_TYPEHINT"): The element to drag.
			xoffset (int): The horizontal offset to drag by.
			yoffset (int): The vertical offset to drag by.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def key_down(self, value: str, element: Optional["WEB_ELEMENT_TYPEHINT"] = None,) -> Self:
		"""
		Performs a key press without releasing it.

		Args:
			value (str): The key to press (e.g., Keys.CONTROL).
			element (Optional["WEB_ELEMENT_TYPEHINT"]): The element to focus before pressing the key.
				If None, the key is pressed without focusing on an element.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def key_up(self, value: str, element: Optional["WEB_ELEMENT_TYPEHINT"] = None,) -> Self:
		"""
		Performs a key release.

		Args:
			value (str): The key to release (e.g., Keys.CONTROL).
			element (Optional["WEB_ELEMENT_TYPEHINT"]): The element to focus before releasing the key.
				If None, the key is released without focusing on an element.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def move_to_element(self, to_element: "WEB_ELEMENT_TYPEHINT",) -> Self:
		"""
		Moves the mouse to the middle of the specified element.

		Args:
			to_element ("WEB_ELEMENT_TYPEHINT"): The element to move to.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def move_to_element_with_offset(self, to_element: "WEB_ELEMENT_TYPEHINT", xoffset: int, yoffset: int,) -> Self:
		"""
		Moves the mouse to an offset from the center of an element.

		Args:
			to_element ("WEB_ELEMENT_TYPEHINT"): The element to move to.
			xoffset (int): The horizontal offset from the element's center.
			yoffset (int): The vertical offset from the element's center.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def pause(self, seconds: Union[float, int],) -> Self:
		"""
		Pauses the execution for a specified duration.

		Args:
			seconds (Union[float, int]): The duration to pause in seconds.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def perform(self) -> None:
		"""
		Performs all stored actions.
		"""
		
		...
	
	@abstractmethod
	def release(self, on_element: Optional["WEB_ELEMENT_TYPEHINT"] = None,) -> Self:
		"""
		Releases a held mouse button.

		Args:
			on_element (Optional["WEB_ELEMENT_TYPEHINT"]): The element on which to release the button.
				If None, releases at the current mouse position.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def scroll_by_amount(self, delta_x: int, delta_y: int,) -> Self:
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
	def scroll_from_origin(self, origin: ScrollOrigin, delta_x: int, delta_y: int,) -> Self:
		"""
		Scrolls from a specific origin "Point" by a given offset.

		Args:
			origin (ScrollOrigin): The origin "Point" to start scrolling from.
			delta_x (int): The horizontal scroll amount.
			delta_y (int): The vertical scroll amount.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def scroll_to_element(self, element: "WEB_ELEMENT_TYPEHINT",) -> Self:
		"""
		Scrolls the view to bring the element into view.

		Args:
			element ("WEB_ELEMENT_TYPEHINT"): The element to scroll to.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def send_keys(self, keys_to_send: str,) -> Self:
		"""
		Sends keys to the current focused element.

		Args:
			keys_to_send (str): The keys to send.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...
	
	@abstractmethod
	def send_keys_to_element(self, element: "WEB_ELEMENT_TYPEHINT", keys_to_send: str,) -> Self:
		"""
		Sends keys to a specific element.

		Args:
			element ("WEB_ELEMENT_TYPEHINT"): The element to send keys to.
			keys_to_send (str): The keys to send.

		Returns:
			AbstractActionChains: The instance of ActionChains for method chaining.
		"""
		
		...


class AbstractHumanLikeActionChains(AbstractActionChains):
	"""
	Abstract base class for human-like action chains.

	Extends AbstractActionChains with methods that simulate more
	natural, less robotic user interactions.
	"""
	
	@abstractmethod
	def hm_move(self, start_position: "Point", end_position: "Point",) -> Self:
		"""
		Moves the mouse cursor from a start to an end position in a human-like curve.

		Args:
			start_position ("Point"): The starting coordinates.
			end_position ("Point"): The ending coordinates.

		Returns:
			AbstractHumanLikeActionChains: The instance for method chaining.
		"""
		
		...
	
	@abstractmethod
	def hm_move_by_offset(self, start_position: "Point", xoffset: int, yoffset: int) -> Tuple[Self, "Point"]:
		"""
		Moves the mouse cursor by a given offset from a starting "Point" in a human-like way.

		Args:
			start_position ("Point"): The starting coordinates of the mouse.
			xoffset (int): The horizontal offset to move by.
			yoffset (int): The vertical offset to move by.

		Returns:
			Tuple[Self, "Point"]: A tuple containing the instance for
			method chaining and the final "Point" coordinates of the cursor.
		"""
		
		...
	
	@abstractmethod
	def hm_move_to_element(self, start_position: "Point", element: "WEB_ELEMENT_TYPEHINT") -> Tuple[Self, "Point"]:
		"""
		Moves the mouse cursor to the center of an element in a human-like way.

		Args:
			start_position ("Point"): The starting coordinates of the mouse.
			element ("WEB_ELEMENT_TYPEHINT"): The target element to move to.

		Returns:
			Tuple[Self, "Point"]: A tuple containing the instance for
			method chaining and the final "Point" coordinates of the cursor.
		"""
		
		...
	
	@abstractmethod
	def hm_move_to_element_with_offset(
			self,
			start_position: "Point",
			element: "WEB_ELEMENT_TYPEHINT",
			xoffset: int,
			yoffset: int
	) -> Tuple[Self, "Point"]:
		"""
		Moves the mouse cursor to a specific offset within an element in a human-like way.

		Args:
			start_position ("Point"): The starting coordinates of the mouse.
			element ("WEB_ELEMENT_TYPEHINT"): The target element.
			xoffset (int): The horizontal offset from the element's top-left corner.
			yoffset (int): The vertical offset from the element's top-left corner.

		Returns:
			Tuple[Self, "Point"]: A tuple containing the instance for
			method chaining and the final "Point" coordinates of the cursor.
		"""
		
		...
	
	@abstractmethod
	def hm_move_to_element_with_random_offset(self, start_position: "Point", element: "WEB_ELEMENT_TYPEHINT",) -> Tuple[Self, "Point"]:
		"""
		Moves the mouse cursor to a random "Point" within an element in a human-like way.

		Args:
			start_position ("Point"): The starting coordinates of the mouse.
			element ("WEB_ELEMENT_TYPEHINT"): The target element to move to.

		Returns:
			Tuple[Self, "Point"]: A tuple containing the instance for
			method chaining and the final "Point" coordinates of the cursor.
		"""
		
		...
	
	@abstractmethod
	def hm_scroll(self, delta_x: int, delta_y: int, origin: Optional[ScrollOrigin] = None,) -> Self:
		"""
		Simulates smooth, human-like scrolling.

		Args:
			delta_x (int): The horizontal distance to scroll.
			delta_y (int): The vertical distance to scroll.
			origin (Optional[ScrollOrigin]): The origin "Point" for scrolling. If None, it's determined automatically.

		Returns:
			AbstractHumanLikeActionains: The instance for method chaining.
		"""
		
		...
	
	@abstractmethod
	def hm_scroll_to_element(
			self,
			element: "WEB_ELEMENT_TYPEHINT",
			additional_lower_y_offset: int = 0,
			additional_upper_y_offset: int = 0,
			additional_right_x_offset: int = 0,
			additional_left_x_offset: int = 0,
			origin: Optional[ScrollOrigin] = None,
	) -> Self:
		"""
		Scrolls smoothly to bring an element into view, avoiding viewport edges.

		Args:
			element ("WEB_ELEMENT_TYPEHINT"): The target element to scroll to.
			additional_lower_y_offset (int): Additional offset from the bottom edge of the viewport.
			additional_upper_y_offset (int): Additional offset from the top edge of the viewport.
			additional_right_x_offset (int): Additional offset from the right edge of the viewport.
			additional_left_x_offset (int): Additional offset from the left edge of the viewport.
			origin (Optional[ScrollOrigin]): The origin "Point" for scrolling. If None, it's determined automatically.

		Returns:
			AbstractHumanLikeActionChains: The instance for method chaining.
		"""
		
		...
	
	@abstractmethod
	def hm_text_input(self, text: str,) -> Self:
		"""
		Simulates human-like text input with variable delays.

		Args:
			text (str): The text to be typed.

		Returns:
			AbstractHumanLikeActionChains: The instance for method chaining.
		"""
		
		...
