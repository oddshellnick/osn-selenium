from typing import Any, Optional
from abc import ABC, abstractmethod


class AbstractCoreTimeoutsMixin(ABC):
	"""Mixin responsible for timeouts and waits."""
	
	@abstractmethod
	def implicitly_wait(self, time_to_wait: float) -> None:
		"""
		Sets an implicit wait time.

		Args:
			time_to_wait (float): The amount of time to wait in seconds.
		"""
		
		...
	
	@abstractmethod
	def set_driver_timeouts(
			self,
			page_load_timeout: float,
			implicit_wait_timeout: float,
			script_timeout: float,
	) -> None:
		"""
		Sets all main driver timeouts.

		Args:
			page_load_timeout (float): Timeout for page loads in seconds.
			implicit_wait_timeout (float): Timeout for implicit waits in seconds.
			script_timeout (float): Timeout for asynchronous scripts in seconds.
		"""
		
		...
	
	@abstractmethod
	def set_page_load_timeout(self, time_to_wait: float) -> None:
		"""
		Sets the timeout for a page load to complete.

		Args:
			time_to_wait (float): The timeout in seconds.
		"""
		
		...
	
	@abstractmethod
	def set_script_timeout(self, time_to_wait: float) -> None:
		"""
		Sets the timeout for asynchronous script execution.

		Args:
			time_to_wait (float): The timeout in seconds.
		"""
		
		...
	
	@abstractmethod
	def set_timeouts(self, timeouts: Any) -> None:
		"""
		Sets the timeouts for the driver.

		Args:
			timeouts (Any): The timeouts configuration object.
		"""
		
		...
	
	@abstractmethod
	def timeouts(self) -> Any:
		"""
		Gets the timeouts object for the current session.

		Returns:
			Any: An object for managing driver timeouts.
		"""
		
		...
	
	@abstractmethod
	def update_times(
			self,
			temp_implicitly_wait: Optional[float] = None,
			temp_page_load_timeout: Optional[float] = None,
			temp_script_timeout: Optional[float] = None,
	) -> None:
		"""
		Temporarily updates driver timeouts for a single operation.

		Args:
			temp_implicitly_wait (Optional[float]): Temporary implicit wait timeout in seconds.
			temp_page_load_timeout (Optional[float]): Temporary page load timeout in seconds.
			temp_script_timeout (Optional[float]): Temporary script timeout in seconds.
		"""
		
		...
