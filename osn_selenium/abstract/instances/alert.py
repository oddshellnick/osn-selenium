from abc import ABC, abstractmethod
from selenium.webdriver.common.alert import Alert as legacyAlert


__all__ = ["AbstractAlert"]


class AbstractAlert(ABC):
	"""
	Abstract base class for an alert dialog.

	Defines the interface for interacting with JavaScript alerts,
	prompts, and confirmation dialogs.
	"""
	
	@abstractmethod
	def accept(self) -> None:
		"""
		Accepts the alert.
		"""
		
		...
	
	@abstractmethod
	def dismiss(self) -> None:
		"""
		Dismisses the alert.
		"""
		
		...
	
	@property
	@abstractmethod
	def legacy(self) -> legacyAlert:
		"""
		Returns the underlying legacy Selenium Alert instance.

		This provides a way to access the original Selenium object for operations
		not covered by this abstract interface.

		Returns:
			legacyAlert: The legacy Selenium Alert object.
		"""
		
		...
	
	@abstractmethod
	def send_keys(self, keysToSend: str) -> None:
		"""
		Sends keys to the alert's prompt.

		Args:
			keysToSend (str): The text to send to the prompt.
		"""
		
		...
	
	@abstractmethod
	def text(self) -> str:
		"""
		The text of the alert.

		Returns:
			str: The text displayed in the alert.
		"""
		
		...
