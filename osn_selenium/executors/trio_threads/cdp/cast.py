import trio
from osn_selenium.base_mixin import TrioThreadMixin
from typing import (
	Any,
	Callable,
	Dict,
	Optional
)
from osn_selenium.executors.unified.cdp.cast import (
	UnifiedCastCDPExecutor
)
from osn_selenium.abstract.executors.cdp.cast import (
	AbstractCastCDPExecutor
)


__all__ = ["CastCDPExecutor"]


class CastCDPExecutor(UnifiedCastCDPExecutor, TrioThreadMixin, AbstractCastCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedCastCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self, presentation_url: Optional[str] = None) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)(presentation_url=presentation_url)
	
	async def set_sink_to_use(self, sink_name: str) -> None:
		return await self.sync_to_trio(sync_function=self._set_sink_to_use_impl)(sink_name=sink_name)
	
	async def start_desktop_mirroring(self, sink_name: str) -> None:
		return await self.sync_to_trio(sync_function=self._start_desktop_mirroring_impl)(sink_name=sink_name)
	
	async def start_tab_mirroring(self, sink_name: str) -> None:
		return await self.sync_to_trio(sync_function=self._start_tab_mirroring_impl)(sink_name=sink_name)
	
	async def stop_casting(self, sink_name: str) -> None:
		return await self.sync_to_trio(sync_function=self._stop_casting_impl)(sink_name=sink_name)
