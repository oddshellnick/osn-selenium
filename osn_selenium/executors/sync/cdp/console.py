from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.console import (
	UnifiedConsoleCDPExecutor
)
from osn_selenium.abstract.executors.cdp.console import (
	AbstractConsoleCDPExecutor
)


__all__ = ["ConsoleCDPExecutor"]


class ConsoleCDPExecutor(UnifiedConsoleCDPExecutor, AbstractConsoleCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedConsoleCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear_messages(self) -> None:
		return self._clear_messages_impl()
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def enable(self) -> None:
		return self._enable_impl()
