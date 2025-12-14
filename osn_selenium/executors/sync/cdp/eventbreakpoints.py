from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.eventbreakpoints import (
	AbstractEventBreakpointsCDPExecutor
)


class EventBreakpointsCDPExecutor(AbstractEventBreakpointsCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def disable(self) -> None:
		return self._execute_function("EventBreakpoints.disable", locals())
	
	def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._execute_function("EventBreakpoints.removeInstrumentationBreakpoint", locals())
	
	def set_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._execute_function("EventBreakpoints.setInstrumentationBreakpoint", locals())
