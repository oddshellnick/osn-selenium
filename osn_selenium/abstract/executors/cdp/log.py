from typing import Any, List
from abc import ABC, abstractmethod


class AbstractLogCDPExecutor(ABC):
	@abstractmethod
	def clear(self) -> None:
		...
	
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def start_violations_report(self, config: List[Any]) -> None:
		...
	
	@abstractmethod
	def stop_violations_report(self) -> None:
		...
