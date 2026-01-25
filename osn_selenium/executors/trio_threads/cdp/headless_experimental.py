import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	Optional,
	Tuple
)
from osn_selenium.executors.unified.cdp.headless_experimental import (
	UnifiedHeadlessExperimentalCDPExecutor
)
from osn_selenium.abstract.executors.cdp.headless_experimental import (
	AbstractHeadlessExperimentalCDPExecutor
)


__all__ = ["HeadlessExperimentalCDPExecutor"]


class HeadlessExperimentalCDPExecutor(
		UnifiedHeadlessExperimentalCDPExecutor,
		TrioThreadMixin,
		AbstractHeadlessExperimentalCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedHeadlessExperimentalCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def begin_frame(
			self,
			frame_time_ticks: Optional[float] = None,
			interval: Optional[float] = None,
			no_display_updates: Optional[bool] = None,
			screenshot: Optional[Dict[str, Any]] = None
	) -> Tuple[bool, Optional[str]]:
		return await self.sync_to_trio(sync_function=self._begin_frame_impl)(
				frame_time_ticks=frame_time_ticks,
				interval=interval,
				no_display_updates=no_display_updates,
				screenshot=screenshot
		)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
