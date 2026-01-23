from typing import Any, Optional
from abc import ABC, abstractmethod


__all__ = ["AbstractCoreCaptureMixin"]


class AbstractCoreCaptureMixin(ABC):
	"""Mixin responsible for screenshots, page source, and printing."""
	
	@abstractmethod
	def get_screenshot_as_base64(self) -> str:
		"""
		Gets a screenshot of the current window as a base64-encoded string.

		Returns:
			str: The base64-encoded screenshot image.
		"""
		
		...
	
	@abstractmethod
	def get_screenshot_as_file(self, filename: str) -> bool:
		"""
		Saves a screenshot to a file. This is an alias for save_screenshot.

		Args:
			filename (str): The full path of the file to save to.

		Returns:
			bool: True if successful, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def get_screenshot_as_png(self) -> bytes:
		"""
		Gets a screenshot of the current window as binary data.

		Returns:
			bytes: The screenshot image in PNG format.
		"""
		
		...
	
	@abstractmethod
	def page_source(self) -> str:
		"""
		Gets the source of the current page.

		Returns:
			str: The source code of the current page.
		"""
		
		...
	
	@abstractmethod
	def print_page(self, print_options: Optional[Any] = None) -> str:
		"""
		Prints the current page to a PDF.

		Args:
			print_options (Optional[Any]): Options for printing the page.

		Returns:
			str: A base64-encoded string of the PDF.
		"""
		
		...
	
	@abstractmethod
	def save_screenshot(self, filename: str) -> bool:
		"""
		Saves a screenshot of the current window to a file.

		Args:
			filename (str): The full path of the file to save the screenshot to.

		Returns:
			bool: True if successful, False otherwise.
		"""
		
		...
