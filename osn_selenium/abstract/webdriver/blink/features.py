from typing import Any, Dict
from abc import ABC, abstractmethod


__all__ = ["AbstractBlinkFeaturesMixin"]


class AbstractBlinkFeaturesMixin(ABC):
	"""
	Abstract mixin defining the interface for specific Blink browser features.

	Includes functionality for handling permissions, launching apps, and retrieving
	browser issue messages.
	"""
	
	@abstractmethod
	def get_issue_message(self) -> Any:
		"""
		Retrieves the current issue message or status from the browser, if any.

		Returns:
			Any: The issue message object or string.
		"""
		
		...
	
	@abstractmethod
	def launch_app(self, id: str) -> Dict[str, Any]:
		"""
		Launches an installed application within the browser by its ID.

		Args:
			id (str): The identifier of the application to launch.

		Returns:
			Dict[str, Any]: A dictionary containing the result of the launch operation.
		"""
		
		...
	
	@abstractmethod
	def set_permissions(self, name: str, value: str) -> None:
		"""
		Sets a specific permission for the browser context.

		Args:
			name (str): The name of the permission (e.g., "camera", "microphone").
			value (str): The value to set (e.g., "granted", "denied").
		"""
		
		...
