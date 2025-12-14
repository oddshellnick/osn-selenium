from typing import Any, Dict
from abc import ABC, abstractmethod
from osn_selenium.abstract.executors.cdp.target import (
	AbstractTargetCDPExecutor
)


class AbstractCDPExecutor(ABC):
	@abstractmethod
	def execute(self, cmd: str, cmd_args: Dict[str, Any]) -> Any:
		"""
		Executes a Chrome DevTools Protocol (CDP) command.

		This method allows direct interaction with the browser's underlying DevTools Protocol,
		enabling fine-grained control over browser behavior, network, page rendering, and more.

		Args:
			cmd (str): The name of the CDP command to execute (e.g., "Page.navigate", "Network.enable", "Emulation.setDeviceMetricsOverride").
			cmd_args (Dict[str, Any]): A Dictionary of arguments specific to the given CDP command.
				The structure and required keys depend on the `cmd` being executed, as defined
				by the Chrome DevTools Protocol specification.

		Returns:
			Any: The result of the CDP command execution. The type and structure of the
				returned value depend on the specific `cmd` and its defined return type
				in the CDP specification.
		"""
		
		...
	
	@property
	@abstractmethod
	def target(self) -> AbstractTargetCDPExecutor:
		...
