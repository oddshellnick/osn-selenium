import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.event_breakpoints import (
	UnifiedEventBreakpointsCDPExecutor
)
from osn_selenium.abstract.executors.cdp.event_breakpoints import (
	AbstractEventBreakpointsCDPExecutor
)


__all__ = ["EventBreakpointsCDPExecutor"]


class EventBreakpointsCDPExecutor(
		UnifiedEventBreakpointsCDPExecutor,
		TrioThreadMixin,
		AbstractEventBreakpointsCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedEventBreakpointsCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def remove_instrumentation_breakpoint(self, event_name: str) -> None:
		return await self.sync_to_trio(sync_function=self._remove_instrumentation_breakpoint_impl)(event_name=event_name)
	
	async def set_instrumentation_breakpoint(self, event_name: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_instrumentation_breakpoint_impl)(event_name=event_name)
