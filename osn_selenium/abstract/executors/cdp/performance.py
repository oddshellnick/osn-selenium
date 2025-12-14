from abc import ABC, abstractmethod
from typing import Any, List, Optional


class AbstractPerformanceCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self, time_domain: Optional[str] = None) -> None:
		...
	
	@abstractmethod
	def get_metrics(self) -> List[Any]:
		...
	
	@abstractmethod
	def set_time_domain(self, time_domain: str) -> None:
		...
