from abc import ABC, abstractmethod
from typing import (
	Any,
	Callable,
	Mapping
)
from selenium.webdriver.common.bidi.script import (
	Script as legacyScript
)


__all__ = ["AbstractScript"]


class AbstractScript(ABC):
	"""
	Abstract base class for script execution and management.

	Defines the interface for executing JavaScript, handling console messages,
	and managing pinned scripts.
	"""
	
	@abstractmethod
	def add_console_message_handler(self, handler: Callable) -> None:
		"""
		Adds a handler for console messages.

		Args:
			handler (Callable): The callback function to handle console messages.
		"""
		
		...
	
	@abstractmethod
	def add_javascript_error_handler(self, handler: Callable) -> None:
		"""
		Adds a handler for JavaScript errors.

		Args:
			handler (Callable): The callback function to handle errors.
		"""
		
		...
	
	@abstractmethod
	def execute(self, script: str, *args: Any) -> Mapping:
		"""
		Executes a script.

		Args:
			script (str): The script to execute.
			*args (Any): Arguments to pass to the script.

		Returns:
			Mapping: The result of the script execution.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyScript:
		"""
		Returns the underlying legacy Selenium Script instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyScript: The legacy Selenium Script object.
		"""
		
		...
	
	@abstractmethod
	def pin(self, script: str) -> str:
		"""
		Pins a script for faster execution.

		Args:
			script (str): The JavaScript code to pin.

		Returns:
			str: The ID of the pinned script.
		"""
		
		...
	
	@abstractmethod
	def remove_console_message_handler(self, id: str) -> None:
		"""
		Removes a console message handler.

		Args:
			id (str): The ID of the handler to remove.
		"""
		
		...
	
	@abstractmethod
	def unpin(self, script_id: str) -> None:
		"""
		Unpins a previously pinned script.

		Args:
			script_id (str): The ID of the script to unpin.
		"""
		
		...
