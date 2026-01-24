from selenium import webdriver
from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from selenium.webdriver.common.bidi.session import Session
from osn_selenium._typehints import (
	ARCHITECTURES_TYPEHINT
)
from selenium.webdriver.remote.errorhandler import ErrorHandler
from osn_selenium.abstract.executors.cdp import AbstractCDPExecutor
from selenium.webdriver.remote.locator_converter import LocatorConverter
from selenium.webdriver.remote.remote_connection import RemoteConnection
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor
from selenium.webdriver.remote.webdriver import (
	WebDriver as legacyWebDriver
)


__all__ = ["AbstractCoreBaseMixin"]


class AbstractCoreBaseMixin(ABC):
	"""
	Abstract base mixin providing core WebDriver functionality and session management.
	"""
	
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
	
	@property
	@abstractmethod
	def architecture(self) -> ARCHITECTURES_TYPEHINT:
		"""
		Returns the architecture of the driver.

		Returns:
			ARCHITECTURE_TYPEHINT: The architecture name.
		"""
		
		...
	
	@property
	@abstractmethod
	def capabilities(self) -> Dict[str, Any]:
		"""
		Returns the capabilities of the current session as reported by the driver.

		Returns:
			Dict[str, Any]: A dictionary of session capabilities.
		"""
		
		...
	
	@property
	@abstractmethod
	def caps(self) -> Dict[str, Any]:
		"""
		The direct representation of session capabilities.

		Returns:
			Dict[str, Any]: Current session capabilities.
		"""
		
		...
	
	@caps.setter
	@abstractmethod
	def caps(self, value: Dict[str, Any]) -> None:
		"""
		Sets the session capabilities.

		Args:
			value (Dict[str, Any]): Dictionary of capabilities.
		"""
		
		...
	
	@property
	@abstractmethod
	def cdp(self) -> AbstractCDPExecutor:
		"""
		Returns the CDP (Chrome DevTools Protocol) executor.

		Returns:
			AbstractCDPExecutor: The CDP executor instance used for sending
			commands directly to the browser via the DevTools protocol.
		"""
		
		...
	
	@property
	@abstractmethod
	def command_executor(self) -> RemoteConnection:
		"""
		Gets the remote connection manager used for executing commands.

		Returns:
			RemoteConnection: The remote connection instance.
		"""
		
		...
	
	@command_executor.setter
	@abstractmethod
	def command_executor(self, value: RemoteConnection) -> None:
		"""
		Sets the remote connection manager used for executing commands.

		Args:
			value (RemoteConnection): The remote connection instance.
		"""
		
		...
	
	@property
	@abstractmethod
	def driver(self) -> Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]:
		"""
		Returns the underlying Selenium WebDriver instance.

		Returns:
			Optional[Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox]]: The driver instance, or None if not started.
		"""
		
		...
	
	@property
	@abstractmethod
	def error_handler(self) -> ErrorHandler:
		"""
		The error handler associated with the current session.

		Returns:
			ErrorHandler: The error handler instance.
		"""
		
		...
	
	@error_handler.setter
	@abstractmethod
	def error_handler(self, value: ErrorHandler) -> None:
		"""
		Sets the error handler for the session.

		Args:
			value (ErrorHandler): The new error handler instance.
		"""
		
		...
	
	@abstractmethod
	def execute(self, driver_command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		"""
		Sends a command to be executed by the remote driver.

		Args:
			driver_command (str): The name of the command to execute.
			params (Optional[Dict[str, Any]]): A dictionary of parameters for the command.

		Returns:
			Dict[str, Any]: The response from the driver.
		"""
		
		...
	
	@property
	@abstractmethod
	def is_active(self) -> bool:
		"""
		Checks if the WebDriver instance is currently running.

		Returns:
			bool: True if the driver is active, False otherwise.
		"""
		
		...
	
	@property
	@abstractmethod
	def javascript(self) -> AbstractJSExecutor:
		"""
		Returns the JavaScript executor for this WebDriver instance.

		Returns:
			AbstractJSExecutor: The JavaScript executor instance.
		"""
		
		...
	
	@property
	@abstractmethod
	def locator_converter(self) -> LocatorConverter:
		"""
		The converter used for translating locators into WebDriver protocols.

		Returns:
			LocatorConverter: The locator converter instance.
		"""
		
		...
	
	@locator_converter.setter
	@abstractmethod
	def locator_converter(self, value: LocatorConverter) -> None:
		"""
		Sets the locator converter instance.

		Args:
			value (LocatorConverter): The new locator converter.
		"""
		
		...
	
	@property
	@abstractmethod
	def name(self) -> str:
		"""
		Returns the name of the underlying browser (e.g., 'chrome', 'firefox').

		Returns:
			str: The name of the browser.
		"""
		
		...
	
	@property
	@abstractmethod
	def pinned_scripts(self) -> Dict[str, Any]:
		"""
		A dictionary of scripts pinned to the current session.

		Returns:
			Dict[str, Any]: Pinned scripts and their handles.
		"""
		
		...
	
	@pinned_scripts.setter
	@abstractmethod
	def pinned_scripts(self, value: Dict[str, Any]) -> None:
		"""
		Sets the pinned scripts for the session.

		Args:
			value (Dict[str, Any]): Dictionary of scripts to pin.
		"""
		
		...
	
	@abstractmethod
	def session(self) -> Session:
		"""
		Internal method to access the current BiDi session object.

		Returns:
			Session: The session object.
		"""
		
		...
	
	@property
	@abstractmethod
	def session_id(self) -> Optional[str]:
		"""
		The unique session ID assigned by the browser driver.

		Returns:
			Optional[str]: The session identifier.
		"""
		
		...
	
	@session_id.setter
	@abstractmethod
	def session_id(self, value: Optional[str]) -> None:
		"""
		Sets the unique session ID.

		Args:
			value (Optional[str]): The new session identifier.
		"""
		
		...
