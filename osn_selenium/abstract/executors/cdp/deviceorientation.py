from typing import Any
from abc import ABC, abstractmethod


class AbstractDeviceOrientationCDPExecutor(ABC):
	@abstractmethod
	def clear_device_orientation_override(self) -> None:
		...
	
	@abstractmethod
	def set_device_orientation_override(self, alpha: float, beta: float, gamma: float) -> None:
		...
