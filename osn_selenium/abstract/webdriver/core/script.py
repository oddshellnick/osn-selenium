from abc import ABC, abstractmethod
from typing import Any, List, Optional
from osn_selenium.abstract.instances.script import AbstractScript


__all__ = ["AbstractCoreScriptMixin"]


class AbstractCoreScriptMixin(ABC):
	"""Mixin responsible for Javascript execution and script management."""
	
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
