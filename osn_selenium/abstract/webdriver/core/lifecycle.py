from abc import ABC, abstractmethod
from osn_selenium.models import WindowRect
from typing import (
	Any,
	Dict,
	Optional,
	Union
)
from osn_selenium.flags.models.base import BrowserFlags
from selenium.webdriver.remote.remote_connection import RemoteConnection


__all__ = ["AbstractCoreLifecycleMixin"]


class AbstractCoreLifecycleMixin(ABC):
	"""Mixin responsible for driver lifecycle, creation, session, and connection management."""
	
	@abstractmethod
	def close_webdriver(self) -> None:
		"""
		Closes the WebDriver instance and all associated windows.
		"""
		
		...
	
	@abstractmethod
	def quit(self) -> None:
		"""
		Quits the driver and closes every associated window.
		"""
		
		...
	
	@abstractmethod
	def remote_connect_driver(self, command_executor: Union[str, RemoteConnection]) -> None:
		"""
		Connects to a remote WebDriver server.

		Args:
			command_executor (Union[str, RemoteConnection]): The URL of the remote server or a RemoteConnection object.
		"""
		
		...
	
	@abstractmethod
	def restart_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Closes the current WebDriver instance and starts a new one.

		Args:
			flags (Optional[BrowserFlags]): Browser flags for the new instance.
			window_rect (Optional[WindowRect]): Window dimensions for the new instance.
		"""
		
		...
	
	@abstractmethod
	def start_client(self) -> None:
		"""
		Starts the underlying webdriver client.
		"""
		
		...
	
	@abstractmethod
	def start_session(self, capabilities: Dict[str, Any]) -> None:
		"""
		Starts a new WebDriver session with the given capabilities.

		Args:
			capabilities (Dict[str, Any]): A dictionary of desired capabilities.
		"""
		
		...
	
	@abstractmethod
	def start_webdriver(
			self,
			flags: Optional[BrowserFlags] = None,
			window_rect: Optional[WindowRect] = None,
	) -> None:
		"""
		Starts the WebDriver instance.

		Args:
			flags (Optional[BrowserFlags]): Browser flags to apply on startup.
			window_rect (Optional[WindowRect]): Initial window dimensions and position.
		"""
		
		...
	
	@abstractmethod
	def stop_client(self) -> None:
		"""
		Stops the underlying webdriver client.
		"""
		
		...
