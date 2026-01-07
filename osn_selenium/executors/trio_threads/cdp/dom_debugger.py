from typing import (
	Any,
	Callable,
	Coroutine,
	Dict,
	List,
	Optional
)
from osn_selenium.abstract.executors.cdp.dom_debugger import (
	AbstractDomDebuggerCDPExecutor
)


class DomDebuggerCDPExecutor(AbstractDomDebuggerCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def get_event_listeners(
			self,
			object_id: str,
			depth: Optional[int] = None,
			pierce: Optional[bool] = None
	) -> List[Any]:
		return await self._execute_function("DOMDebugger.getEventListeners", locals())
	
	async def remove_dom_breakpoint(self, node_id: int, type_: str) -> None:
		return await self._execute_function("DOMDebugger.removeDOMBreakpoint", locals())
	
	async def remove_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		return await self._execute_function("DOMDebugger.removeEventListenerBreakpoint", locals())
	
	async def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		return await self._execute_function("DOMDebugger.removeInstrumentationBreakpoint", locals())
	
	async def remove_xhr_breakpoint(self, url: str) -> None:
		return await self._execute_function("DOMDebugger.removeXHRBreakpoint", locals())
	
	async def set_break_on_csp_violation(self, violation_types: List[str]) -> None:
		return await self._execute_function("DOMDebugger.setBreakOnCSPViolation", locals())
	
	async def set_dom_breakpoint(self, node_id: int, type_: str) -> None:
		return await self._execute_function("DOMDebugger.setDOMBreakpoint", locals())
	
	async def set_event_listener_breakpoint(self, event_name: str, target_name: Optional[str] = None) -> None:
		return await self._execute_function("DOMDebugger.setEventListenerBreakpoint", locals())
	
	async def set_instrumentation_breakpoint(self, event_name: str) -> None:
		return await self._execute_function("DOMDebugger.setInstrumentationBreakpoint", locals())
	
	async def set_xhr_breakpoint(self, url: str) -> None:
		return await self._execute_function("DOMDebugger.setXHRBreakpoint", locals())
