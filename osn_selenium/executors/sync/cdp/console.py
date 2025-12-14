from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.console import (
	AbstractConsoleCDPExecutor
)


class ConsoleCDPExecutor(AbstractConsoleCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear_messages(self) -> None:
		return self._execute_function("Console.clearMessages", locals())
	
	def disable(self) -> None:
		return self._execute_function("Console.disable", locals())
	
	def enable(self) -> None:
		return self._execute_function("Console.enable", locals())
