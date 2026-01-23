from abc import ABC, abstractmethod
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple
)


__all__ = ["AbstractProfilerCDPExecutor"]


class AbstractProfilerCDPExecutor(ABC):
	@abstractmethod
	def disable(self) -> None:
		...
	
	@abstractmethod
	def enable(self) -> None:
		...
	
	@abstractmethod
	def get_best_effort_coverage(self) -> List[Dict[str, Any]]:
		...
	
	@abstractmethod
	def set_sampling_interval(self, interval: int) -> None:
		...
	
	@abstractmethod
	def start(self) -> None:
		...
	
	@abstractmethod
	def start_precise_coverage(
			self,
			call_count: Optional[bool] = None,
			detailed: Optional[bool] = None,
			allow_triggered_updates: Optional[bool] = None
	) -> float:
		...
	
	@abstractmethod
	def stop(self) -> Dict[str, Any]:
		...
	
	@abstractmethod
	def stop_precise_coverage(self) -> None:
		...
	
	@abstractmethod
	def take_precise_coverage(self) -> Tuple[List[Dict[str, Any]], float]:
		...
