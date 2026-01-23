from abc import abstractmethod
from selenium import webdriver
from typing import Optional, Union
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.abstract.webdriver.core.base import (
	AbstractCoreBaseMixin
)


__all__ = ["AbstractBlinkBaseMixin"]


class AbstractBlinkBaseMixin(AbstractCoreBaseMixin):
	"""
	Abstract mixin defining the base interface for Blink-based WebDrivers (Chrome, Edge).

	This mixin establishes the contract for managing the browser executable path,
	debugging connection details, and the underlying Selenium driver instance.
	"""
	
	@property
	@abstractmethod
	def browser_exe(self) -> Optional[PATH_TYPEHINT]:
		"""
		Returns the file path to the browser executable.

		Returns:
			Optional[PATH_TYPEHINT]: The path to the executable,
			or None if not managed by this instance.
		"""
		
		...
	
	@property
	@abstractmethod
	def debugging_ip(self) -> Optional[str]:
		"""
		Returns the IP address used for the remote debugging protocol.

		Returns:
			Optional[str]: The debugging IP address (e.g., "127.0.0.1"), or None if not set.
		"""
		
		...
	
	@property
	@abstractmethod
	def debugging_port(self) -> Optional[int]:
		"""
		Returns the port number used for the remote debugging protocol.

		Returns:
			Optional[int]: The debugging port, or None if not set.
		"""
		
		...
	
	@property
	@abstractmethod
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge]]:
		"""
		Returns the underlying Selenium WebDriver instance.

		Returns:
			Optional[Union[webdriver.Chrome, webdriver.Edge]]: The driver instance,
			or None if not started.
		"""
		
		...
	
	@abstractmethod
	def set_start_page_url(self, start_page_url: str) -> None:
		"""
		Sets the URL that the browser should navigate to upon startup.

		Args:
			start_page_url (str): The URL to set as the start page.
		"""
		
		...
