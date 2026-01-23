import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.device_access import (
	UnifiedDeviceAccessCDPExecutor
)
from osn_selenium.abstract.executors.cdp.device_access import (
	AbstractDeviceAccessCDPExecutor
)


__all__ = ["DeviceAccessCDPExecutor"]


class DeviceAccessCDPExecutor(
		UnifiedDeviceAccessCDPExecutor,
		TrioThreadMixin,
		AbstractDeviceAccessCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedDeviceAccessCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def cancel_prompt(self, id_: str) -> None:
		return await self.sync_to_trio(sync_function=self._cancel_prompt_impl)(id_=id_)
	
	async def disable(self) -> None:
		return await self.sync_to_trio(sync_function=self._disable_impl)()
	
	async def enable(self) -> None:
		return await self.sync_to_trio(sync_function=self._enable_impl)()
	
	async def select_prompt(self, id_: str, device_id: str) -> None:
		return await self.sync_to_trio(sync_function=self._select_prompt_impl)(id_=id_, device_id=device_id)
