from abc import ABC, abstractmethod


__all__ = ["AbstractBackgroundServiceCDPExecutor"]


class AbstractBackgroundServiceCDPExecutor(ABC):
	@abstractmethod
	def clear_events(self, service: str) -> None:
		...
	
	@abstractmethod
	def set_recording(self, should_record: bool, service: str) -> None:
		...
	
	@abstractmethod
	def start_observing(self, service: str) -> None:
		...
	
	@abstractmethod
	def stop_observing(self, service: str) -> None:
		...
