from typing import Any
from abc import ABC, abstractmethod


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
