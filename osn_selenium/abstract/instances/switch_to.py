from typing import Optional, Union
from abc import ABC, abstractmethod
from selenium.webdriver.common.alert import Alert
from osn_selenium.abstract.instances.web_element import AbstractWebElement
from selenium.webdriver.remote.switch_to import (
	SwitchTo as legacySwitchTo
)


__all__ = ["AbstractSwitchTo"]


class AbstractSwitchTo(ABC):
	"""
	Abstract base class for context switching.

	Defines the interface for switching between frames, windows, and alerts.
	"""
	
	@abstractmethod
	def active_element(self) -> AbstractWebElement:
		"""
		Returns the element with focus, or the body if no element has focus.

		Returns:
			AbstractWebElement: The currently active WebElement.
		"""
		
		...
	
	@abstractmethod
	def alert(self) -> Alert:
		"""
		Switches to the currently active alert.

		Returns:
			Alert: The Alert object for the active alert.
		"""
		
		...
	
	@abstractmethod
	def default_content(self) -> None:
		"""
		Switches focus to the default content of a page.
		"""
		
		...
	
	@abstractmethod
	def frame(self, frame_reference: Union[str, int, AbstractWebElement]) -> None:
		"""
		Switches focus to the specified frame.

		Args:
			frame_reference (Union[str, int, AbstractWebElement]): The name, index, or WebElement of the frame.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacySwitchTo:
		"""
		Returns the underlying legacy Selenium SwitchTo instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacySwitchTo: The legacy Selenium SwitchTo object.
		"""
		
		...
	
	@abstractmethod
	def new_window(self, type_hint: Optional[str] = None) -> None:
		"""
		Creates a new window and switches to it.

		Args:
			type_hint (Optional[str]): Specifies the type of new window, e.g., 'tab' or 'window'.
		"""
		
		...
	
	@abstractmethod
	def parent_frame(self) -> None:
		"""
		Switches focus to the parent frame.
		"""
		
		...
	
	@abstractmethod
	def window(self, window_name: str) -> None:
		"""
		Switches focus to the specified window.

		Args:
			window_name (str): The name or window handle of the window to switch to.
		"""
		
		...
