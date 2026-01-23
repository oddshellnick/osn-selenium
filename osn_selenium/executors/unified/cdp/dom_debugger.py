from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)


__all__ = ["UnifiedDomDebuggerCDPExecutor"]


class UnifiedDomDebuggerCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _get_event_listeners_impl(
			self,
			object_id: str,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._execute_function(
				"DOMDebugger.getEventListeners",
				{"object_id": object_id, "depth": depth, "pierce": pierce}
		)
	
	def _remove_dom_breakpoint_impl(self, node_id: int, type_: str) -> None:
		return self._execute_function("DOMDebugger.removeDOMBreakpoint", {"node_id": node_id, "type_": type_})
	
	def _remove_event_listener_breakpoint_impl(self, event_name: str, target_name: Optional[str] = None) -> None:
		return self._execute_function(
				"DOMDebugger.removeEventListenerBreakpoint",
				{"event_name": event_name, "target_name": target_name}
		)
	
	def _remove_instrumentation_breakpoint_impl(self, event_name: str) -> None:
		return self._execute_function(
				"DOMDebugger.removeInstrumentationBreakpoint",
				{"event_name": event_name}
		)
	
	def _remove_xhr_breakpoint_impl(self, url: str) -> None:
		return self._execute_function("DOMDebugger.removeXHRBreakpoint", {"url": url})
	
	def _set_break_on_csp_violation_impl(self, violation_types: List[str]) -> None:
		return self._execute_function(
				"DOMDebugger.setBreakOnCSPViolation",
				{"violation_types": violation_types}
		)
	
	def _set_dom_breakpoint_impl(self, node_id: int, type_: str) -> None:
		return self._execute_function("DOMDebugger.setDOMBreakpoint", {"node_id": node_id, "type_": type_})
	
	def _set_event_listener_breakpoint_impl(self, event_name: str, target_name: Optional[str] = None) -> None:
		return self._execute_function(
				"DOMDebugger.setEventListenerBreakpoint",
				{"event_name": event_name, "target_name": target_name}
		)
	
	def _set_instrumentation_breakpoint_impl(self, event_name: str) -> None:
		return self._execute_function("DOMDebugger.setInstrumentationBreakpoint", {"event_name": event_name})
	
	def _set_xhr_breakpoint_impl(self, url: str) -> None:
		return self._execute_function("DOMDebugger.setXHRBreakpoint", {"url": url})
