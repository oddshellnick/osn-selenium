from abc import ABC, abstractmethod


__all__ = ["AbstractMediaCDPExecutor"]


class AbstractMediaCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
