from abc import ABC, abstractmethod


__all__ = ["AbstractConsoleCDPExecutor"]


class AbstractConsoleCDPExecutor(ABC):
	@abstractmethod
	def clear_messages(self) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
