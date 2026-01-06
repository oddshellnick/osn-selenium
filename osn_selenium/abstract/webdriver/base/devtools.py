from abc import ABC, abstractmethod
from contextlib import (
	AbstractAsyncContextManager
)
from typing import (
	Any,
	AsyncGenerator,
	Dict,
	Tuple
)
from osn_selenium.abstract.instances.network import AbstractNetwork
from selenium.webdriver.remote.bidi_connection import BidiConnection
from selenium.webdriver.remote.websocket_connection import WebSocketConnection


class AbstractDevToolsMixin(ABC):
	"""Mixin responsible for CDP, DevTools, and Network interactions."""
	
	@abstractmethod
	def bidi_connection(self) -> AbstractAsyncContextManager[AsyncGenerator[BidiConnection, Any]]:
		"""
		Returns an context manager for a BiDi (WebDriver Bi-Directional) connection.

		Returns:
			AbstractAsyncContextManager[AsyncGenerator[BidiConnection, Any]]: The BiDi connection context manager.
		"""
		
		...
	
	@abstractmethod
	def capabilities(self) -> Dict[str, Any]:
		"""
		Returns the capabilities of the current session.

		Returns:
			Dict[str, Any]: A dictionary of session capabilities.
		"""
		
		...
	
	@abstractmethod
	def execute_cdp_cmd(self, cmd: str, cmd_args: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Executes a Chrome DevTools Protocol command.

		Args:
			cmd (str): The CDP command to execute.
			cmd_args (Dict[str, Any]): The arguments for the command.

		Returns:
			Dict[str, Any]: The result of the command execution.
		"""
		
		...
	
	@abstractmethod
	def network(self) -> AbstractNetwork:
		"""
		Provides access to the network interception and monitoring interface.

		Returns:
			AbstractNetwork: An object for interacting with network events.
		"""
		
		...
	
	@abstractmethod
	def start_devtools(self) -> Tuple[Any, WebSocketConnection]:
		"""
		Starts a connection to the browser's developer tools.

		Returns:
			Tuple[Any, WebSocketConnection]: A tuple containing the DevTools session info and WebSocket connection.
		"""
		
		...
