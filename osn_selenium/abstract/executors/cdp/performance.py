from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional
)


__all__ = ["AbstractPerformanceCDPExecutor"]


class AbstractPerformanceCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self, time_domain: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def get_metrics(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def set_time_domain(self, time_domain: str) -> None:
		...
