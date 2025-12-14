from typing import (
	Any,
	Callable,
	Coroutine,
	Dict
)
from osn_selenium.abstract.executors.cdp.device_orientation import (
	AbstractDeviceOrientationCDPExecutor
)


class DeviceOrientationCDPExecutor(AbstractDeviceOrientationCDPExecutor):
	def __init__(
			self,
			execute_function: Callable[[str, Dict[str, Any]], Coroutine[Any, Any, Any]]
	):
		self._execute_function = execute_function
	
	async def clear_device_orientation_override(self) -> None:
		return await self._execute_function("DeviceOrientation.clearDeviceOrientationOverride", locals())
	
	async def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		return await self._execute_function("DeviceOrientation.setDeviceOrientationOverride", locals())
