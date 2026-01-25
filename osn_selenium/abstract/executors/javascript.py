from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from osn_selenium.javascript.models import JS_Scripts
from selenium.webdriver.remote.webelement import WebElement
from osn_selenium.javascript.fingerprint import FingerprintSettings
from osn_selenium.models import (
	Point,
	Position,
	Rectangle,
	Size
)


__all__ = ["AbstractJSExecutor"]


class AbstractJSExecutor(ABC):
	"""
	Abstract base class for executing JavaScript commands in a browser context.

	This class defines the interface for interacting with JavaScript scripts,
	including checking element visibility, getting computed styles, and managing
	viewport properties.
	"""
	
	@abstractmethod
	def check_element_in_viewport(self, element: WebElement) -> bool:
		"""
		Checks if the element is currently visible within the viewport.

		Args:
			element (WebElement): The element to check.

		Returns:
			bool: True if the element is fully within the viewport,
				otherwise False.
		"""
		
		...
	
	@abstractmethod
	def execute(self, script: str, *args: Any) -> Any:
		"""
		Executes a JavaScript snippet.

		Args:
			script (str): The JavaScript code to execute.
			*args (Any): Arguments to pass to the script.

		Returns:
			Any: The result of the script execution.
		"""
		
		...
	
	@abstractmethod
	def get_document_scroll_size(self) -> Size:
		"""
		Gets the total scrollable width and height of the document.

		Returns:
			Size: An object containing the scroll width and height.
		"""
		
		...
	
	@abstractmethod
	def get_element_css_style(self, element: WebElement) -> Dict[str, str]:
		"""
		Retrieves all computed CSS properties for an element.

		Args:
			element (WebElement): The element to get the style from.

		Returns:
			Dict[str, str]: A dictionary of CSS properties and their values.
		"""
		
		...
	
	@abstractmethod
	def get_element_rect_in_viewport(self, element: WebElement) -> Rectangle:
		"""
		Gets the element's position and size relative to the viewport.

		Args:
			element (WebElement): The element to measure.

		Returns:
			Rectangle: An object with the x, y, width, and height of the
				element.
		"""
		
		...
	
	@abstractmethod
	def get_random_element_point(self, element: WebElement) -> Optional[Point]:
		"""
		Gets a random point within an element, relative to the viewport.

		Args:
			element (WebElement): The element to find a point in.

		Returns:
			Optional[Point]: An object with the x and y coordinates of the random
				point relative to the viewport, or None if no point is found.
		"""
		
		...
	
	@abstractmethod
	def get_random_element_point_in_viewport(self, element: WebElement, step: int = 1) -> Optional[Position]:
		"""
		Calculates a random point within an element's visible area.

		Args:
			element (WebElement): The element to find a point within.
			step (int): The grid step for sampling points. Defaults to 1.

		Returns:
			Optional[Position]: An object with x and y coordinates relative to
				the element's top-left corner, or None if no point is found.
		"""
		
		...
	
	@abstractmethod
	def get_viewport_position(self) -> Position:
		"""
		Gets the viewport's current scroll position relative to the document.

		Returns:
			Position: An object containing the x (horizontal) and y
				(vertical) scroll offsets.
		"""
		
		...
	
	@abstractmethod
	def get_viewport_rect(self) -> Rectangle:
		"""
		Gets the viewport's position and size relative to the document.

		Returns:
			Rectangle: An object with the scroll offsets (x, y) and
				dimensions (width, height) of the viewport.
		"""
		
		...
	
	@abstractmethod
	def get_viewport_size(self) -> Size:
		"""
		Gets the current dimensions of the browser's viewport.

		Returns:
			Size: An object containing the width and height of the viewport.
		"""
		
		...
	
	@abstractmethod
	def open_new_tab(self, link: str = "") -> None:
		"""
		Opens a new browser tab.

		Args:
			link (str): The URL to open. If empty, a blank tab is opened.
				Defaults to "".
		"""
		
		...
	
	@property
	@abstractmethod
	def scripts(self) -> JS_Scripts:
		"""
		Provides access to the loaded JavaScript snippets.

		Returns:
			JS_Scripts: An object holding the predefined JS scripts.
		"""
		
		...
	
	@abstractmethod
	def start_fingerprint_detection(self, fingerprint_settings: FingerprintSettings) -> None:
		"""
		Initiate fingerprint detection based on the provided settings.

		Args:
			fingerprint_settings (FingerprintSettings): The settings used for fingerprint detection.
		"""
		
		...
	
	@abstractmethod
	def stop_window_loading(self) -> None:
		"""
		Stops the current page from loading.
		"""
		
		...
