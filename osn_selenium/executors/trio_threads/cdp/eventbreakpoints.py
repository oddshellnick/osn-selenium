from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.eventbreakpoints import (
	AbstractEventBreakpointsCDPExecutor
)


class AsyncEventBreakpointsCDPExecutor(AbstractEventBreakpointsCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def disable(self) -> None:
		return await self._execute_function("EventBreakpoints.disable", locals())
	
	async def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		return await self._execute_function("EventBreakpoints.removeInstrumentationBreakpoint", locals())
	
	async def set_instrumentation_breakpoint(self, event_name: str) -> None:
		return await self._execute_function("EventBreakpoints.setInstrumentationBreakpoint", locals())
