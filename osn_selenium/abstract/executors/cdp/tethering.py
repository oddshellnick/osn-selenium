from abc import ABC, abstractmethod


__all__ = ["AbstractTetheringCDPExecutor"]


class AbstractTetheringCDPExecutor(ABC):
	@abstractmethod
	def bind(self, port: int) -> None:
		...
	
	@abstractmethod
	def unbind(self, port: int) -> None:
		...
