from selenium import webdriver
from abc import ABC, abstractmethod
from selenium.webdriver.common.bidi.session import Session
from osn_selenium.instances.types import WEB_ELEMENT_TYPEHINT
from selenium.webdriver.remote.remote_connection import RemoteConnection
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Set,
	Tuple,
	Union
)
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)


class AbstractBaseMixin(ABC):
	@abstractmethod
	def _ensure_driver(self) -> Optional[legacyWebDriver]:
		"""
		Internal method to ensure the WebDriver instance is running before an operation.

		Returns:
			Optional[legacyWebDriver]: The driver instance if verified, otherwise None.

		Raises:
			RuntimeError: If the driver is not started.
		"""
		
		...
	
	@abstractmethod
	def _session(self) -> Session:
		"""
		Internal method to access the current session object.

		Returns:
			Session: The session object.
		"""
		
		...
	
	def _unwrap_args(self, arg: Any) -> Any:
		...
	
	def _wrap_result(self, result: Any) -> Union[
		WEB_ELEMENT_TYPEHINT,
		List[WEB_ELEMENT_TYPEHINT],
		Dict[Any, WEB_ELEMENT_TYPEHINT],
		Set[WEB_ELEMENT_TYPEHINT],
		Tuple[WEB_ELEMENT_TYPEHINT, ...],
		Any,
	]:
		...
	
	@abstractmethod
	def command_executor(self) -> RemoteConnection:
		"""
		Gets the remote connection manager used for executing commands.

		Returns:
			RemoteConnection: The remote connection instance.
		"""
		
		...
	
	@abstractmethod
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]:
		"""
		Returns the underlying Selenium WebDriver instance.

		Returns:
			Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]: The driver instance, or None if not started.
		"""
		
		...
	
	@abstractmethod
	def is_active(self) -> bool:
		"""
		Checks if the WebDriver instance is currently running.

		Returns:
			bool: True if the driver is active, False otherwise.
		"""
		
		...
	
	@abstractmethod
	def name(self) -> str:
		"""
		Returns the name of the underlying browser (e.g., 'chrome', 'firefox').

		Returns:
			str: The name of the browser.
		"""
		
		...
