from abc import ABC, abstractmethod


__all__ = ["AbstractDeviceAccessCDPExecutor"]


class AbstractDeviceAccessCDPExecutor(ABC):
	@abstractmethod
	def cancel_prompt(self, id_: str) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def select_prompt(self, id_: str, device_id: str) -> None:
		...
