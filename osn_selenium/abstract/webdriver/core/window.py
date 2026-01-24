from abc import ABC, abstractmethod
from typing import (
	List,
	Literal,
	Optional,
	Union
)
from osn_selenium.models import (
	Position,
	Rectangle,
	Size
)
from osn_selenium.abstract.instances.switch_to import AbstractSwitchTo


__all__ = ["AbstractCoreWindowMixin"]


class AbstractCoreWindowMixin(ABC):
	"""Mixin responsible for window management, switching, and geometry."""
	
	@abstractmethod
	def close(self) -> None:
		"""
		Closes the current window.
		"""
		
		...
	
	@abstractmethod
	def close_all_windows(self) -> None:
		"""
		Closes all open windows in the current session.
		"""
		
		...
	
	@abstractmethod
	def close_window(self, window: Optional[Union[str, int]] = None) -> None:
		"""
		Closes a specific window by handle or index, or the current window if not specified.
		If the closed window was the current one, attempts to switch to the last remaining window.

		Args:
			window (Optional[Union[str, int]]): The window handle (str) or index (int) to close.
		"""
		
		...
	
	@abstractmethod
	def current_window_handle(self) -> str:
		"""
		Returns the handle of the current window.

		Returns:
			str: The handle of the current window.
		"""
		
		...
	
	@abstractmethod
	def fullscreen_window(self) -> None:
		"""
		Invokes the window manager-specific "full screen" operation.
		"""
		
		...
	
	@abstractmethod
	def get_window_handle(self, window: Optional[Union[str, int]] = None) -> str:
		"""
		Gets the handle of a specific window by handle or index.

		Args:
			window (Optional[Union[str, int]]): The specific window handle (str) or index (int).
				If None, defaults to the current window.

		Returns:
			str: The window handle.

		Raises:
			IndexError: If the numeric window index is out of range.
			RuntimeError: If no window handles are available.
		"""
		
		...
	
	@abstractmethod
	def get_window_position(self, window_handle: str = "current") -> Position:
		"""
		Gets the position of a window.

		Args:
			window_handle (str): The handle of the window.

		Returns:
			Position: An object containing the 'x' and 'y' coordinates of the window.
		"""
		
		...
	
	@abstractmethod
	def get_window_rect(self) -> Rectangle:
		"""
		Gets the position and size of the current window.

		Returns:
			Rectangle: An object with 'x', 'y', 'width', and 'height' properties.
		"""
		
		...
	
	@abstractmethod
	def get_window_size(self, window_handle: str = "current") -> Size:
		"""
		Gets the size of a window.

		Args:
			window_handle (str): The handle of the window.

		Returns:
			Size: An object containing the 'width' and 'height' of the window.
		"""
		
		...
	
	@abstractmethod
	def maximize_window(self) -> None:
		"""
		Maximizes the current window.
		"""
		
		...
	
	@abstractmethod
	def minimize_window(self) -> None:
		"""
		Minimizes the current window.
		"""
		
		...
	
	@abstractmethod
	def orientation(self) -> Literal["LANDSCAPE", "PORTRAIT"]:
		"""
		Gets the current orientation of the browser.

		Returns:
			Literal["LANDSCAPE", "PORTRAIT"]: The current orientation.
		"""
		
		...
	
	@abstractmethod
	def set_orientation(self, value: Literal["LANDSCAPE", "PORTRAIT"]) -> None:
		"""
		Sets the browser orientation.

		Args:
			value (Literal["LANDSCAPE", "PORTRAIT"]): The new orientation.
		"""
		
		...
	
	@abstractmethod
	def set_window_position(self, x: int, y: int, window_handle: str = "current") -> Position:
		"""
		Sets the position of a window.

		Args:
			x (int): The x-coordinate of the top-left corner.
			y (int): The y-coordinate of the top-left corner.
			window_handle (str): The handle of the window to move.

		Returns:
			Position: An object representing the new window position.
		"""
		
		...
	
	@abstractmethod
	def set_window_rect(
			self,
			x: Optional[int] = None,
			y: Optional[int] = None,
			width: Optional[int] = None,
			height: Optional[int] = None,
	) -> Rectangle:
		"""
		Sets the position and size of the current window.

		Args:
			x (Optional[int]): The x-coordinate of the top-left corner.
			y (Optional[int]): The y-coordinate of the top-left corner.
			width (Optional[int]): The new width of the window.
			height (Optional[int]): The new height of the window.

		Returns:
			Rectangle: An object representing the new window rectangle.
		"""
		
		...
	
	@abstractmethod
	def set_window_size(self, width: int, height: int, window_handle: str = "current") -> None:
		"""
		Sets the size of a window.

		Args:
			width (int): The new width in pixels.
			height (int): The new height in pixels.
			window_handle (str): The handle of the window to resize.
		"""
		
		...
	
	@abstractmethod
	def switch_to(self) -> AbstractSwitchTo:
		"""
		Returns an object to switch context to another frame, window, or alert.

		Returns:
			AbstractSwitchTo: The SwitchTo instance for context switching.
		"""
		
		...
	
	@abstractmethod
	def window_handles(self) -> List[str]:
		"""
		Returns the handles of all windows within the current session.

		Returns:
			List[str]: A list of window handles.
		"""
		
		...
