from typing import Any, Callable, Dict


__all__ = ["UnifiedConsoleCDPExecutor"]


class UnifiedConsoleCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_messages_impl(self) -> None:
		return self._execute_function("Console.clearMessages", {})
	
	def _disable_impl(self) -> None:
		return self._execute_function("Console.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Console.enable", {})
