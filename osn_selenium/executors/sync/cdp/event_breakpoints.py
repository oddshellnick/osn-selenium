from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.event_breakpoints import (
	UnifiedEventBreakpointsCDPExecutor
)
from osn_selenium.abstract.executors.cdp.event_breakpoints import (
	AbstractEventBreakpointsCDPExecutor
)


__all__ = ["EventBreakpointsCDPExecutor"]


class EventBreakpointsCDPExecutor(
		UnifiedEventBreakpointsCDPExecutor,
		AbstractEventBreakpointsCDPExecutor
):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedEventBreakpointsCDPExecutor.__init__(self, execute_function=execute_function)
	
	def disable(self) -> None:
		return self._disable_impl()
	
	def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._remove_instrumentation_breakpoint_impl(event_name=event_name)
	
	def set_instrumentation_breakpoint(self, event_name: str) -> None:
		return self._set_instrumentation_breakpoint_impl(event_name=event_name)
