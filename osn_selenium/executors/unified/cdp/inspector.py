from typing import Any, Callable, Dict


__all__ = ["UnifiedInspectorCDPExecutor"]


class UnifiedInspectorCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("Inspector.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Inspector.enable", {})
