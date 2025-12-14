from typing import Any, Callable, Dict
from osn_selenium.abstract.executors.cdp.deviceorientation import (
	AbstractDeviceOrientationCDPExecutor
)


class DeviceOrientationCDPExecutor(AbstractDeviceOrientationCDPExecutor):
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def clear_device_orientation_override(self) -> None:
		return self._execute_function("DeviceOrientation.clearDeviceOrientationOverride", locals())
	
	def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		return self._execute_function("DeviceOrientation.setDeviceOrientationOverride", locals())
