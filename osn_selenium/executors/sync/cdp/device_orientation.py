from typing import Any, Callable, Dict
from osn_selenium.executors.unified.cdp.device_orientation import (
	UnifiedDeviceOrientationCDPExecutor
)
from osn_selenium.abstract.executors.cdp.device_orientation import (
	AbstractDeviceOrientationCDPExecutor
)


__all__ = ["DeviceOrientationCDPExecutor"]


class DeviceOrientationCDPExecutor(
		UnifiedDeviceOrientationCDPExecutor,
		AbstractDeviceOrientationCDPExecutor
):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		UnifiedDeviceOrientationCDPExecutor.__init__(self, execute_function=execute_function)
	
	def clear_device_orientation_override(self) -> None:
		return self._clear_device_orientation_override_impl()
	
	def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		return self._set_device_orientation_override_impl(alpha=alpha, beta=beta, gamma=gamma)
