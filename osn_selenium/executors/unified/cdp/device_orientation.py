from typing import Any, Callable, Dict


__all__ = ["UnifiedDeviceOrientationCDPExecutor"]


class UnifiedDeviceOrientationCDPExecutor:
	def __init__(self, execute_function: Callable[[str, Dict[str, Any]], Any]):
		self._execute_function = execute_function
	
	def _clear_device_orientation_override_impl(self) -> None:
		return self._execute_function("DeviceOrientation.clearDeviceOrientationOverride", {})
	
	def _set_device_orientation_override_impl(self, alpha: float, beta: float, gamma: float) -> None:
		return self._execute_function(
				"DeviceOrientation.setDeviceOrientationOverride",
				{"alpha": alpha, "beta": beta, "gamma": gamma}
		)
