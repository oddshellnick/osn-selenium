from typing import (
	Any,
	Callable,
	Dict,
	List,
	Optional
)
from osn_selenium.executors.unified.cdp.dom_debugger import (
	UnifiedDomDebuggerCDPExecutor
)
from osn_selenium.abstract.executors.cdp.dom_debugger import (
	AbstractDomDebuggerCDPExecutor
)


__all__ = ["DomDebuggerCDPExecutor"]


class DomDebuggerCDPExecutor(UnifiedDomDebuggerCDPExecutor, AbstractDomDebuggerCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedDomDebuggerCDPExecutor.__init__(self, execute_function=execute_function)
	
	def get_event_listeners(
			self,
			object_id: str,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> List[Dict[str, Any]]:
		return self._get_event_listeners_impl(object_id=object_id, depth=depth, pierce=pierce)
	
	def remove_dom_breakpoint(self, node_id: int, type_: str) -> None:
		return self._remove_dom_breakpoint_impl(node_id=node_id, type_=type_)
	
	def remove_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		return self._remove_event_listener_breakpoint_impl(event_name=event_name, target_name=target_name)
	
	def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._remove_instrumentation_breakpoint_impl(event_name=event_name)
	
	def remove_xhr_breakpoint(self, url: str) -> None:
		return self._remove_xhr_breakpoint_impl(url=url)
	
	def set_break_on_csp_violation(self, violation_types: List[str]) -> None:
		return self._set_break_on_csp_violation_impl(violation_types=violation_types)
	
	def set_dom_breakpoint(self, node_id: int, type_: str) -> None:
		return self._set_dom_breakpoint_impl(node_id=node_id, type_=type_)
	
	def set_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		return self._set_event_listener_breakpoint_impl(event_name=event_name, target_name=target_name)
	
	def set_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._set_instrumentation_breakpoint_impl(event_name=event_name)
	
	def set_xhr_breakpoint(self, url: str) -> None:
		return self._set_xhr_breakpoint_impl(url=url)
