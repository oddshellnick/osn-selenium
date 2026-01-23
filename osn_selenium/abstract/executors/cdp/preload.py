from abc import ABC, abstractmethod


__all__ = ["AbstractPreloadCDPExecutor"]


class AbstractPreloadCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
