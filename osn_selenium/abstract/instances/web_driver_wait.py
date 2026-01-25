from typing import Any, Callable
from abc import ABC, abstractmethod
from selenium.webdriver.support.wait import (
	WebDriverWait as legacyWebDriverWait
)


__all__ = ["AbstractWebDriverWait"]


class AbstractWebDriverWait(ABC):
	"""
	Abstract base class for WebDriver wait implementations.

	Provides the interface for waiting until a condition is met or a timeout occurs.
	"""
	
	@abstractmethod
	def legacy(self) -> legacyWebDriverWait:
		"""
		Returns the underlying Selenium WebDriverWait instance.

		Returns:
			legacyWebDriverWait: The original Selenium wait object.
		"""
		
		...
	
	@abstractmethod
	def until(self, method: Callable[[Any], Any], message: str = "") -> Any:
		"""
		Waits until the method returns a non-false value.

		Args:
			method (Callable[[Any], Any]): The condition to evaluate.
			message (str): Optional message for TimeoutException.

		Returns:
			Any: The return value of the method.
		"""
		
		...
	
	@abstractmethod
	def until_not(self, method: Callable[[Any], Any], message: str = "") -> Any:
		"""
		Waits until the method returns a false value.

		Args:
			method (Callable[[Any], Any]): The condition to evaluate.
			message (str): Optional message for TimeoutException.

		Returns:
			Any: The return value of the method.
		"""
		
		...
