from typing import Any, Callable, Dict


__all__ = ["UnifiedEventBreakpointsCDPExecutor"]


class UnifiedEventBreakpointsCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _disable_impl(self) -> None:
		return self._execute_function("EventBreakpoints.disable", {})
	
	def _remove_instrumentation_breakpoint_impl(self, event_name: str) -> None:
		return self._execute_function(
				"EventBreakpoints.removeInstrumentationBreakpoint",
				{"event_name": event_name}
		)
	
	def _set_instrumentation_breakpoint_impl(self, event_name: str) -> None:
		return self._execute_function(
				"EventBreakpoints.setInstrumentationBreakpoint",
				{"event_name": event_name}
		)
