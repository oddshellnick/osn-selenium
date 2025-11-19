from typing import Any, List
from abc import ABC, abstractmethod


__all__ = ["AbstractBlinkLoggingMixin"]


class AbstractBlinkLoggingMixin(ABC):
	"""
	Abstract mixin defining the interface for accessing browser logs.

	Allows retrieving specific log types (e.g., browser, performance, client) supported
	by the Blink-based browser.
	"""
	
	@abstractmethod
	def get_log(self, log_type: str) -> Any:
		"""
		Retrieves the logs for a specific log type.

		Args:
			log_type (str): The type of log to retrieve (must be one of the available log types).

		Returns:
			Any: The log entries, typically a list of dictionaries containing log messages.
		"""
		
		...
	
	@abstractmethod
	def log_types(self) -> List[str]:
		"""
		Retrieves the list of available log types.

		Returns:
			List[str]: A list of strings representing the available log types
			(e.g., ['browser', 'driver', 'client', 'performance']).
		"""
		
		...
