from abc import ABC, abstractmethod


__all__ = ["AbstractDeviceOrientationCDPExecutor"]


class AbstractDeviceOrientationCDPExecutor(ABC):
	@abstractmethod
	def clear_device_orientation_override(self) -> None:
		...
	
	@abstractmethod
	def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		...
