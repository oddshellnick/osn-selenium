from typing import Any, Callable, Dict


__all__ = ["UnifiedTetheringCDPExecutor"]


class UnifiedTetheringCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _bind_impl(self, port: int) -> None:
		return self._execute_function("Tethering.bind", {"port": port})
	
	def _unbind_impl(self, port: int) -> None:
		return self._execute_function("Tethering.unbind", {"port": port})
