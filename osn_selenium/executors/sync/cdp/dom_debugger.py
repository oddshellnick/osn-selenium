from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.dom_debugger import (
	AbstractDomDebuggerCDPExecutor
)


class DomDebuggerCDPExecutor(AbstractDomDebuggerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def get_event_listeners(
			self,
			object_id: str,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> List[Any]:
		return self._execute_function("DOMDebugger.getEventListeners", locals())
	
	def remove_dom_breakpoint(self, node_id: int, type_: str) -> None:
		return self._execute_function("DOMDebugger.removeDOMBreakpoint", locals())
	
	def remove_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		return self._execute_function("DOMDebugger.removeEventListenerBreakpoint", locals())
	
	def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._execute_function("DOMDebugger.removeInstrumentationBreakpoint", locals())
	
	def remove_xhr_breakpoint(self, url: str) -> None:
		return self._execute_function("DOMDebugger.removeXHRBreakpoint", locals())
	
	def set_break_on_csp_violation(self, violation_types: List[str]) -> None:
		return self._execute_function("DOMDebugger.setBreakOnCSPViolation", locals())
	
	def set_dom_breakpoint(self, node_id: int, type_: str) -> None:
		return self._execute_function("DOMDebugger.setDOMBreakpoint", locals())
	
	def set_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		return self._execute_function("DOMDebugger.setEventListenerBreakpoint", locals())
	
	def set_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._execute_function("DOMDebugger.setInstrumentationBreakpoint", locals())
	
	def set_xhr_breakpoint(self, url: str) -> None:
		return self._execute_function("DOMDebugger.setXHRBreakpoint", locals())
