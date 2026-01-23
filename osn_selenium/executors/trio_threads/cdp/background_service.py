import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.background_service import (
	UnifiedBackgroundServiceCDPExecutor
)
from osn_selenium.abstract.executors.cdp.background_service import (
	AbstractBackgroundServiceCDPExecutor
)


__all__ = ["BackgroundServiceCDPExecutor"]


class BackgroundServiceCDPExecutor(
		UnifiedBackgroundServiceCDPExecutor,
		TrioThreadMixin,
		AbstractBackgroundServiceCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedBackgroundServiceCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear_events(self, service: str) -> None:
		return await self.sync_to_trio(sync_function=self._clear_events_impl)(service=service)
	
	async def set_recording(self, should_record: bool, service: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_recording_impl)(should_record=should_record, service=service)
	
	async def start_observing(self, service: str) -> None:
		return await self.sync_to_trio(sync_function=self._start_observing_impl)(service=service)
	
	async def stop_observing(self, service: str) -> None:
		return await self.sync_to_trio(sync_function=self._stop_observing_impl)(service=service)
