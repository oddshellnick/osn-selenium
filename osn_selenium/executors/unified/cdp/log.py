from typing import (
	Any,
	Callable,
	Dict,
	List
)


__all__ = ["UnifiedLogCDPExecutor"]


class UnifiedLogCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_impl(self) -> None:
		return self._execute_function("Log.clear", {})
	
	def _disable_impl(self) -> None:
		return self._execute_function("Log.disable", {})
	
	def _enable_impl(self) -> None:
		return self._execute_function("Log.enable", {})
	
	def _start_violations_report_impl(self, config: List[Dict[str, Any]]) -> None:
		return self._execute_function("Log.startViolationsReport", {"config": config})
	
	def _stop_violations_report_impl(self) -> None:
		return self._execute_function("Log.stopViolationsReport", {})
