from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.instances.script import AbstractScript
from osn_selenium.abstract.executors.javascript import AbstractJSExecutor


class AbstractScriptMixin(ABC):
	"""Mixin responsible for Javascript execution and script management."""
	
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
	
	@abstractmethod
	def execute_async_script(self, script: str, *args: Any) -> Any:
		"""
		Asynchronously executes JavaScript in the current window/frame.

		Args:
			script (str): The JavaScript to execute.
			*args (Any): Any arguments to pass to the script.

		Returns:
			Any: The value returned by the script's callback.
		"""
		
		...
	
	@abstractmethod
	def execute_script(self, script: str, *args: Any) -> Any:
		"""
		Synchronously executes JavaScript in the current window/frame.

		Args:
			script (str): The JavaScript to execute.
			*args (Any): Any arguments to pass to the script.

		Returns:
			Any: The value returned by the script.
		"""
		
		...
	
	@abstractmethod
	def get_pinned_scripts(self) -> List[str]:
		"""
		Gets a list of all currently pinned scripts.

		Returns:
			List[str]: A list of pinned scripts.
		"""
		
		...
	
	@abstractmethod
	def pin_script(self, script: str, script_key: Optional[Any] = None) -> Any:
		"""
		Pins a script to the browser for faster execution.

		Args:
			script (str): The JavaScript to pin.
			script_key (Optional[Any]): An optional key to identify the script.

		Returns:
			Any: The key associated with the pinned script.
		"""
		
		...
	
	@abstractmethod
	def script(self) -> AbstractScript:
		"""
		Provides access to the script execution interface.

		Returns:
			AbstractScript: An object for managing and executing scripts.
		"""
		
		...
	
	@abstractmethod
	def unpin(self, script_key: Any) -> None:
		"""
		Unpins a previously pinned script.

		Args:
			script_key (Any): The key of the script to unpin.
		"""
		
		...
