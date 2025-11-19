import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.web_audio import (
	UnifiedWebAudioCDPExecutor
)
from osn_selenium.abstract.executors.cdp.web_audio import (
	AbstractWebAudioCDPExecutor
)


__all__ = ["WebAudioCDPExecutor"]


class WebAudioCDPExecutor(
		UnifiedWebAudioCDPExecutor,
		TrioThreadMixin,
		AbstractWebAudioCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedWebAudioCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def get_realtime_data(self, context_id: str) -> Dict[str, Any]:
		return await self.sync_to_trio(sync_function=self._get_realtime_data_impl)(context_id=context_id)
