from abc import ABC, abstractmethod


__all__ = ["AbstractInspectorCDPExecutor"]


class AbstractInspectorCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
