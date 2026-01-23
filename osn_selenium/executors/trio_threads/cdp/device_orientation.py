import trio
from typing import Any, Callable, Dict
from osn_selenium.base_mixin import TrioThreadMixin
from osn_selenium.executors.unified.cdp.device_orientation import (
	UnifiedDeviceOrientationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.device_orientation import (
	AbstractDeviceOrientationCDPExecutor
)


__all__ = ["DeviceOrientationCDPExecutor"]


class DeviceOrientationCDPExecutor(
		UnifiedDeviceOrientationCDPExecutor,
		TrioThreadMixin,
		AbstractDeviceOrientationCDPExecutor
):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Any],
			lock: trio.Lock,
			limiter: trio.CapacityLimiter
	):
		UnifiedDeviceOrientationCDPExecutor.__init__(self, execute_function=execute_function)
		
		TrioThreadMixin.__init__(self, lock=lock, limiter=limiter)
	
	async def clear_device_orientation_override(self) -> None:
		return await self.sync_to_trio(sync_function=self._clear_device_orientation_override_impl)()
	
	async def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		return await self.sync_to_trio(sync_function=self._set_device_orientation_override_impl)(alpha=alpha, beta=beta, gamma=gamma)
