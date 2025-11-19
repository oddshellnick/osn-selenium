from typing import Any, Dict, List
from abc import ABC, abstractmethod


__all__ = ["AbstractLogCDPExecutor"]


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
	def start_violations_report(self, config: List[Dict[str, Any]]) -> None:
		...
	
	@abstractmethod
	def stop_violations_report(self) -> None:
		...
